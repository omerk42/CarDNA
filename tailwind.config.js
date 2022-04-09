module.exports = {
// <<<<<<< HEAD
  // content: ["./index.html","./sign-up.html","./login.html"],
  content: ["./*.html"],
// =======
  content: ["./app/templates/*.html"],
// >>>>>>> 94504090164d5d3ba3b0eba9eb6b11b82b37aaf5
  theme: {
    extend: {
      colors:{
        'body': '#052540',
        'selected-text': '#FFC95A',
        'theme': '#FFB215',
        'nav' : '#404053',
        'secondary': '#9191a4',
        'badge' : '#3f3f51',
        'input-border': '#565666',
        'input': '#2a2a35'
      },
      fontFamily:{
        'poppins':["'Poppins' , 'sans-serif'"]
      },
      backgroundImage: {
        'hero-pattern': "url('/images/Background-Image-5.png')"
      }
    },
  },
  plugins: [],
}
