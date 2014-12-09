module.exports = function(grunt) {
	"use strict";

  grunt.initConfig({
    pkg: grunt.file.readJSON("package.json"),
    uglify: {
      build: {
        src: "static/js/<%= pkg.name %>.js",
        dest: "static/js/<%= pkg.name %>.min.js"
      }
    },
    jshint: {
      individualFiles: ["Gruntfile.js", "static/js/books.js"],
      options: {
        jshintrc: ".jshintrc"
      }
    }
  });

  grunt.loadNpmTasks("grunt-contrib-uglify");
  grunt.loadNpmTasks("grunt-contrib-jshint");

  grunt.registerTask("default", [/*"uglify",*/ "jshint"]);
};