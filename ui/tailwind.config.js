module.exports = {
    purge: ["./index.html", "./src/**/*.{vue,js,ts,jsx,tsx}"],
    darkMode: false,
    content: ["./src/**/*.{html,js}"],
    theme: {
        extend: {
            colors: {
                'dark-red': '#800000'
            }
        },
    },
    variants: {
        extend: {},
    },
    plugins: [
    ],
}
