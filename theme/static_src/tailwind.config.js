// This is a minimal config.
// If you need the full config, get it from here:
// https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
module.exports = {
    purge: [
        // Templates within theme app (e.g. base.html)
        '../templates/**/*.html',
        // Templates in other apps. Uncomment the following line if it matches
        // your project structure or change it to match.
        '../../templates/**/*.html',
    ],
    darkMode: false, // or 'media' or 'class'
    theme: {
        extend: {
            backgroundImage: theme => ({
                'no-data': "url('/static/images/signal_heropattern.svg')",
                'endlessclouds': "url('/static/images/endless-clouds_heropattern.svg')",
                'foundation': "url('/static/images/aztec_heropattern.svg')"
            }),
            animation: {
                'spin-1': 'spin 3s linear infinite',
                'spin-2': 'spin 4s linear infinite',
                'spin-3': 'spin 5s linear infinite',
            }
        },
    },
    variants: {
        extend: {},
    },
    plugins: []
}
