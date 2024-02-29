import { createStore } from 'vuex'
import { postApi } from '@/api'
import { isValidJwt } from '@/authentication'

const store = createStore({
  state() {
      return {
          jwt: '',
          userData: {},
      }
  },
  mutations: {
      setUserData(state, payload) {
          console.log('setUserData payload = ', payload)
          state.userData = payload.userData
      },
      setJwtToken(state, payload) {
          console.log('setJwtToken payload = ', payload)
          localStorage.jwt = payload.jwt
          state.jwt = payload.jwt
      }
  },
  actions: {
      login(context, userData) {
          console.log("login userData = ", userData)
          context.commit('setUserData', { userData })

          return postApi("/login", userData)
            .then(data => { context.commit('setJwtToken', { jwt: data.token }) } )
            .catch(error => {
                console.log('Error Authenticating: ', error)
            })
      },
      tryRecoverJwt(context) {
        if (localStorage.getItem('jwt') !== '') {
            console.log("recovering from localStorage")
            context.commit("setJwtToken", { jwt: localStorage.jwt })
        }
      },
      logout(context) {
          context.commit("setUserData", { userData: {} })
          context.commit("setJwtToken", { jwt: '' })
      }
  },
  modules: {
  },
  getters: {
    isAuthenticated(state) {
      return isValidJwt(state.jwt)
    }
  }
})

export default store
