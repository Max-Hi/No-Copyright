from flask import Flask, jsonify, request, current_app
from flask_cors import CORS
from enum import Enum, auto
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo import MongoClient
from bson.objectid import ObjectId
import jwt
import os
import sys
import logging
from getpass import getpass
import math
from time import perf_counter
import re
import itertools
from pprint import pprint
import getpass
import random

LOCAL_DEV = True
DBHOST = "testdb"

def create_app(test_config=None):
    app = Flask(__name__)
    CORS(app)
    app.secret_key = "debugging" # change before deployment

    app.logger.setLevel(logging.DEBUG)

    # Setting up Mongo DB
    if LOCAL_DEV:
        client = MongoClient(DBHOST)
    else:
        username = os.environ.get('USERNAME')
        password = os.environ.get('PASSWORD')
        client = MongoClient(DBHOST, username=username, password=password)

    db = client.vfm

    @app.cli.command("add_user")
    def add_user():
        username = input("Username: ")
        number_of_users_found = db.users.count_documents({"username": username})
        if number_of_users_found == 1:
            logger.error(f"Tried adding user {username}, but user already present.")
            sys.exit(1)
        if number_of_users_found > 1:
            logger.error(f"Tried adding user {username}, but multiple user with that username already present.")
            sys.exit(1)

        password = getpass()
        password = generate_password_hash(password, 'sha256')
        db.users.insert_one({"username": username, "password": password})
    #    db.createCollection()

    @app.route("/")
    def index():
        return "<h1>This is the NC API!</h1>"

    def authenticated(username: str, password: str) -> bool:
        user = db["users"].find_one({"username": username})
        return check_password_hash(user['password'], password)


    @app.route("/login", methods=["POST"])
    def login():
        data = request.get_json()
        if not data or "username" not in data or "password" not in data or \
                not authenticated(data["username"], data["password"]):
            return {"message": "Invalid credentials", "authenticated": False}, 401
        token = jwt.encode({
            'sub': data["username"],
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(minutes=180)
        }, app.secret_key)
        # logger.info("requested token", token)

        return jsonify({'token': token.decode("UTF-8")})


    def token_required(f):
        @wraps(f)
        def _verify(*args, **kwargs):
            auth_headers = request.headers.get("JWTAuthorization", "").split()

            invalid_message = {
                "message": "Invalid token. Authentication required",
                "authenticated": False
            }
            expired_message = {
                "message": "Expired token. Reauthentication required",
                "authenticated": False
            }

            if len(auth_headers) != 2:
                return invalid_message, 401

            try:
                token = auth_headers[1]
                data = jwt.decode(token, app.secret_key)
                user = db['users'].find_one({'username': data['sub']})

                if not user:
                    app.logger.error("could not find user")
                    return invalid_message, 401

                return f(user, *args, **kwargs)

            except jwt.ExpiredSignatureError as error:
                app.logger.error(str(error))
                return expired_message, 401

            except jwt.InvalidTokenError as error:
                app.logger.error(error)
                return invalid_message, 401

        return _verify


    @app.route("/delete", methods=["POST"])
    @token_required
    def delete(user):
        video_id = request.get_json()["id"]
        _id = ObjectId(video_id)
        for userdata in db.users.find():
            db[userdata["username"]].delete_one({"_id": _id})
        drive = db.videos.find_one({"_id": _id})["filepath"]
        db.videos.delete_one({"_id": _id})
        os.system("rm ../../videos/"+drive+"/"+video_id+".mp4")
        return jsonify({})

    @app.route("/search", methods=["POST"])
    @token_required
    def search(user):
        # `token_required` validates the user, user is object retrieved from db.users with the corresponding username

        # get submitted data from http request
        data = request.get_json()
       

        # conform to mongodb query operator
        data["junktoren"] = {key: "$" + junktor for key, junktor in data["junktoren"].items()}

        tag_searches = []
        for tag in data["tags"]:
            tag_searches.append({"name": tag})

        # create the query lists for the searches
        tag_queries = [{"tags": {"$elemMatch": tag_search}} for tag_search in tag_searches]
        studio_queries = [{"video.studios": studio} for studio in data["studios"]]
        star_queries = [{"video.stars": star} for star in data["stars"]]
        
        # filter metadata for tags, rating and playback_position
        filter_metadata_stage = {"$match": {"$and": [
            ({data["junktoren"]["tags"]: tag_queries} if tag_queries else {}),
            {            "$or": [{"rating": {"$gte": data["minRating"]}}, {"rating": -1}]},
            {"playback_position": dict(zip(["$gte", "$lte"], data["watched"]))},
            ({"$text": {"$search": data["title"]}} if data["title"] else {})
        ]}}

        # get the corresponding video to each metadata
        get_videos_stage = {"$lookup": {
            "from": "videos",
            "localField": "video_id",
            "foreignField": "_id",
            "as": "video"
        }}

        # filter for studios, stars, length, resolution
        filter_videos_stage = {"$match": {"$and": [
            ({data["junktoren"]["studios"]: studio_queries} if studio_queries else {}),
            ({data["junktoren"]["stars"]: star_queries} if star_queries else {}),
            {"video.resolution": {"$gte": data["minResolution"]}},
            {"video.length": dict(zip(["$gte", "$lte"], data["length"]))},
        ]}}

        # TODO this if statement seems redundant, but I did not write it, so please evaluate and possibly remove!!!
        if data["junktoren"]["tags"] == "and":
            cursor = db[user['username']].aggregate([
                filter_metadata_stage,
                get_videos_stage,
                filter_videos_stage,
            ])
        else:
            cursor = db[user['username']].aggregate([
                filter_metadata_stage,
                get_videos_stage,
                filter_videos_stage,
            ])

        results = [{"title": doc["title"],
                    "id": str(doc["video"][0]["_id"]),
                    "metadata_id": str(doc["_id"]),
                    "filepath": doc["video"][0]["filepath"],
                    "studios": doc["video"][0]["studios"],
                    "stars": doc["video"][0]["stars"],
                    "length": doc["video"][0]["length"],
                    "tags": doc["tags"],
                    "rating": doc["rating"],
                    "views": doc["views"],
                    "playback_position": doc["playback_position"],
                    "resolution": doc["video"][0]["resolution"]
                    }
                   for doc in cursor]

        # possibly have tags/ stars/ studios linked to photos, therefore tags/ stars/ studios have id's
        for res in results:
            for tag in res['tags']:
                if '_id' in tag:
                    tag['_id'] = str(tag['_id'])
            for star in res['stars']:
                if '_id' in star:
                    tag['_id'] = str(star['_id'])
            for studio in res['studios']:
                if '_id' in studio:
                    tag['_id'] = str(studio['_id'])

        # shuffle
        if data["sorting"] =="none":
            random.shuffle(results)
        # sorting
        for field in ["tags", "studios", "stars"]:  # The order matters! Which order do we want?
            if data["junktoren"][field] == "or":
                # sorts by the number of tags/studios/stars that were searched for but not in the metadata
                # start = perf_counter()
                results.sort(
                    key=lambda result: len(
                        set(data[field]) - set(db.videos.find_one({"_id": ObjectId(result["id"])})[field])),
                    reverse=data["reversed"])
                # stop = perf_counter()
        if data["sorting"] == "length":
            # start = perf_counter()
            results.sort(key=lambda result: db.videos.find_one({"_id": ObjectId(result["id"])})["length"],
                         reverse=data["reversed"])
            # stop = perf_counter()
        elif data["sorting"] == "rating":
            # start = perf_counter()
            results.sort(
                key=lambda result: db[user["username"]].find_one({"_id": ObjectId(result["metadata_id"])})["rating"],
                reverse=data["reversed"])
            # stop = perf_counter()
        elif data["sorting"] == "relevant":
            # start = perf_counter()
            results.sort(key=lambda result: db.videos.find_one({"_id": ObjectId(result["id"])})["rating"] * math.log(
                db.videos.find_one({"_id": ObjectId(result["id"])})["views"] + 1), reverse=data["reversed"])
            # stop = perf_counter()
        elif data["sorting"] == "none":
            pass  # this is the value for no sorting
        else:
            
            logger.warning("Sorting had an invalid value. ")

        for res in results:
            try:
                jsonify(res)
            except TypeError as e:
                pprint(res)
                print(e)

        return jsonify(results[:250])


    @app.route("/upload", methods=["POST"])
    @token_required
    def uploadLink(user):
        data = request.get_json()

        return jsonify({"message": "not implemented"})


    @app.route("/video", methods=["POST"])
    @token_required
    def video(user):
        data = request.get_json()
        video = db.videos.find_one({"_id": ObjectId(data["id"])})
        metadata = db[user["username"]].find_one({"video_id": video["_id"]})
        video["title"] = metadata["title"]
        video["rating"] = metadata["rating"]
        video["playback_position"] = metadata["playback_position"]
        video["views"] = metadata["views"]
        video["id"] = str(video["_id"])
        del video["_id"]
        video["videoUrl"] = "http://10.8.0.1:5501/videos/" + video["filepath"] + "/" + video["id"] + ".mp4"
        video["tags"] = metadata["tags"]
        video["resolution"] = video["resolution"]
        return video


    def search_coresponding_descriptor(descriptor_searched_for: str, descriptor_match_on: str, match_on_name: str, user):

        if descriptor_searched_for != "tags" and descriptor_match_on != "tags":
            print(descriptor_searched_for, descriptor_match_on)
            cursor = db[user["username"]].aggregate([
                {"$match": {}},
                {"$lookup": {"from": "videos", "foreignField": "_id", "localField": "video_id", "as": "video"}},
                {"$addFields": {"video": {"$first": "$video"}}},
                {"$unwind": "$video." + descriptor_searched_for},
                {"$facet": {
                    "matching": [{"$match": {"video." + descriptor_match_on: match_on_name}},
                                 {"$group": {"_id": "$video." + descriptor_searched_for, "matchingCount": {"$count": {}}}},
                                 {"$addFields": {"count": {"matchingCount": "$matchingCount"}}}],
                    "total": [{"$group": {"_id": "$video." + descriptor_searched_for, "totalCount": {"$count": {}}}},
                              {"$addFields": {"count": {"totalCount": "$totalCount"}}}]
                }},
                {"$project": {"res": {"$concatArrays": ["$matching", "$total"]}}},
                {"$unwind": "$res"},
                {"$group": {"_id": "$res._id", "merged": {"$mergeObjects": "$res.count"}}},
                {"$match": {"merged.matchingCount": {"$exists": True}}},
                {"$match": {"merged.totalCount": {"$gt": 1}}},
                {"$project": {"_id": 1, "ranking":
                    {"$multiply": [{"$divide": ["$merged.matchingCount", "$merged.totalCount"]},
                                   {"$log": ["$merged.matchingCount", 1.1]}]}}},
                {"$sort": {"ranking": -1}}
            ])

        else:
            print("ERROR: incorrect use of search_corresponding_descriptor!")

        return cursor


    @app.route("/tag", methods=["POST"])
    @token_required
    def tagInfo(user):
        data = request.get_json()
        tagname = data["name"]

        star_cursor = search_coresponding_descriptor("stars", "tags", tagname, user)
        star_list = []
        for star in star_cursor:
            if len(star_list) < 30:
                star_list.append(star)
            else:
                break

        studio_cursor = search_coresponding_descriptor("studios", "tags", tagname, user)
        studio_list = []
        for studio in studio_cursor:
            if len(studio_list) < 30:
                studio_list.append(studio)
            else:
                break

        video_cursor = db[user["username"]].aggregate([
            {"$match": {"tags": {"$elemMatch": {"name": tagname}}}},
            {"$lookup": {
                "from": "videos",
                "localField": "video_id",
                "foreignField": "_id",
                "as": "video"
            }},
        ])

        videolist = [{"title": doc["video"][0]["title"],
                      "id": str(doc["video"][0]["_id"]),
                      "metadata_id": str(doc["_id"]),
                      "filepath": doc["video"][0]["filepath"],
                      "studios": doc["video"][0]["studios"],
                      "stars": doc["video"][0]["stars"],
                      "length": doc["video"][0]["length"],
                      "tags": doc["tags"],
                      "rating": doc["rating"],
                      "views": doc["views"],
                      "playback_position": doc["playback_position"],
                      "resolution": doc["video"][0]["resolution"]
                      }
                     for doc in video_cursor][:30]
        videolist.sort(key=lambda x: float(x["rating"]), reverse=True)

        return {"videoList": videolist, "starList": star_list, "studioList": studio_list}


    @app.route("/star", methods=["POST"])
    @token_required
    def starInfo(user):
        data = request.get_json()
        starname = data["name"]

        tag_cursor = search_coresponding_descriptor("tags", "stars", starname, user)
        studio_cursor = search_coresponding_descriptor("studios", "stars", starname, user)

        video_cursor = db[user["username"]].aggregate(
            [{"$lookup": {"from": "videos", "localField": "video_id", "foreignField": "_id", "as": "video"}},
             {"$match": {"video.stars": starname}}
             ])

        videolist = [{"title": doc["video"][0]["title"],
                      "id": str(doc["video"][0]["_id"]),
                      "metadata_id": str(doc["_id"]),
                      "filepath": doc["video"][0]["filepath"],
                      "studios": doc["video"][0]["studios"],
                      "stars": doc["video"][0]["stars"],
                      "length": doc["video"][0]["length"],
                      "tags": doc["tags"],
                      "rating": doc["rating"],
                      "views": doc["views"],
                      "playback_position": doc["playback_position"],
                      "resolution": doc["video"][0]["resolution"]
                      }
                     for doc in video_cursor][:30]
        videolist.sort(key=lambda x: float(x["rating"]), reverse=True)

        return {"videoList": videolist, "tagList": list(tag_cursor)[:30], "studioList": list(studio_cursor)[:30]}

     
    @app.route("/studio", methods=["POST"])
    @token_required
    def studioInfo(user):
        data = request.get_json()
        studioname = data["name"]

        star_cursor = search_coresponding_descriptor("stars", "studios", studioname, user)
        tag_cursor = search_coresponding_descriptor("tags", "studios", studioname, user)

        video_cursor = db[user["username"]].aggregate([
            {"$lookup": {"from": "videos", "localField": "video_id", "foreignField": "_id", "as": "video"}},
            {"$match": {"video.studios": studioname}},
        ])

        videolist = [{"title": doc["video"][0]["title"],
                      "id": str(doc["video"][0]["_id"]),
                      "metadata_id": str(doc["_id"]),
                      "filepath": doc["video"][0]["filepath"],
                      "studios": doc["video"][0]["studios"],
                      "stars": doc["video"][0]["stars"],
                      "length": doc["video"][0]["length"],
                      "tags": doc["tags"],
                      "rating": doc["rating"],
                      "views": doc["views"],
                      "playback_position": doc["playback_position"],
                      "resolution": doc["video"][0]["resolution"]
                      }
                     for doc in video_cursor][:30]
        videolist.sort(key=lambda x: float(x["rating"]), reverse=True)

        return {"videoList": videolist, "starList": list(star_cursor)[:30], "tagList": list(tag_cursor)[:30]}



    @app.route("/studios", methods=["GET"])
    @token_required
    def getStudios(user):
        
        studio_cursor = db[user["username"]].aggregate([
                {"$match": {}},
                {"$lookup": {"from": "videos", "foreignField": "_id", "localField": "video_id", "as": "video"}},
                {"$unwind": "$video.studios"},
                {"$group": {"_id": "$res._id", "merged": {"$mergeObjects": "$res.count"}}},
            ])
        logger.debug("getStudios was called") 

        return {"studioList": []}

    @app.route("/stars", methods=["GET"])
    @token_required
    def getStars(user):
        
        studio_cursor = db[user["username"]].aggregate([
                {"$match": {}},
                {"$lookup": {"from": "videos", "foreignField": "_id", "localField": "video_id", "as": "video"}},
                {"$unwind": "$video.stars"},
            ])
        logger.debug("getStars was called")
        return {"starList": []}

    @app.route("/tags", methods=["GET"])
    @token_required
    def getTags(user):
        
        logger.debug("getTags was called")
        studio_cursor = db.max.aggregate([ 
            {"$match": {}}, 
            {"$lookup": {"from": "videos", "foreignField": "_id", "localField": "video_id", "as": "video"}}, 
            {"$unwind": "$tags"}, 
            {"$group": {"_id": "$tags.name"}}]) # adding "merged" returns nothing - , "merged": {}
        logger.debug("getTags returned "+str(list(studio_cursor)))
        return {"tagList": []}


    # trying to implement metadata editing:
    @app.route("/metadata", methods=["POST"])
    @token_required
    def metadata(user):
        # `token_required` validates the user, user is object retrieved from db.users with the corresponding username
        # get submitted data from http request
        data = request.get_json()

        added_tags = [tag for tag in data["newTags"] if tag and tag[0] != "-"]
        removed_tags = [tag[1:] for tag in data["newTags"] if tag and tag[0] == "-"]

        added_stars = [star for star in data["newStars"] if star and star[0] != "-"]
        removed_stars = [star[1:] for star in data["newStars"] if star and star[0] == "-"]

        added_studios = [studio for studio in data["newStudios"] if studio and studio[0] != "-"]
        removed_studios = [studio[1:] for studio in data["newStudios"] if studio and studio[0] == "-"]

        video = db.videos.find_one({"_id": ObjectId(str(data["id"]))})

        # find metadata for user for corresponding video with data["id"] and update
        if removed_tags:
            db[user["username"]].update_one({"video_id": ObjectId(data["id"])},
                                            {"$pull": {"tags": {"name": tag}} for tag in removed_tags})

        if removed_stars:
            db["videos"].update_one({"_id": ObjectId(data["id"])},
                                    {"$pull": {"stars": {"name": star}} for star in removed_stars})

        if removed_studios:
            db["videos"].update_one({"_id": ObjectId(data["id"])},
                                    {"$pull": {"studios": {"name": studio}} for studio in removed_studios})

        updates = {"$set": {}, "$addToSet": {}}
        updates_global = {"$set": {}, "$addToSet": {}}

        if added_tags:
            updates_global["$addToSet"].update({"tags": {"$each": [tag for tag in added_tags]}})
            # commit to tag collection
            for tag in added_tags: 
                if db["tags"].find_one({"name": tag}) is None:
                    db["tags"].insert_one({"name": tag})

        if added_stars:
            updates_global["$addToSet"].update({"stars": {"$each": [star for star in added_stars]}})
            # commit to star collection
            for star in added_stars: 
                gender = "unknown" #todo
                if db["stars"].find_one({"name": star}) is None:
                    db["stars"].insert_one({"name": star, "gender": gender})

        if added_studios:
            updates_global["$addToSet"].update({"studios": {"$each": [studio for studio in added_studios]}})
            # commit to studio collection
            for studio in added_studios: 
                if db["tags"].find_one({"name": studio}) is None:
                    db["tags"].insert_one({"name": studio})

        if data["newTitle"]:
            updates["$set"].update({"title": data["newTitle"]})

        if data["newPlaybackPosition"]:
            updates["$set"].update({"playback_position": float(data["newPlaybackPosition"]) * 60 / (
                video["length"])})  # *60 because the videolength is in seconds and the user will probably put in min

        if data["newRating"]:
            updates["$set"].update({"rating": float(data["newRating"])})

        db[user["username"]].update_one({"video_id": ObjectId(data["id"])},
                                        updates)
        db["videos"].update_one({"_id": ObjectId(data["id"])},
                                updates_global)

        return {"data": data}

    return app

app = create_app()

