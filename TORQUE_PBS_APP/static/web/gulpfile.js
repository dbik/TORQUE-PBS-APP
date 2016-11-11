// Include gulp
var gulp = require('gulp');

// Include Our Plugins
var jshint = require('gulp-jshint');
var sass = require('gulp-sass');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var rename = require('gulp-rename');
var minifyCss = require('gulp-minify-css');


// Lint Task
gulp.task('lint', function() {
    return gulp.src(['js/src/*.js',
                     'js/src/**/*.js',])
                     //'js/dist/*.js'])
        .pipe(jshint())
        .pipe(jshint.reporter('default'));
});


// Compile Our Sass
gulp.task('sass', function() {
    return gulp.src('scss/*.scss')
        .pipe(sass())
        .pipe(gulp.dest('css'));
});


// Concatenate & Minify JS
gulp.task('minify-js', function() {
    return gulp.src(['js/src/modules/login/module.js',
                     'js/src/modules/shop/module.js',
                     'js/src/modules/main/app.js'])
        .pipe(concat('all.js'))
        .pipe(gulp.dest('js/dist'))
        .pipe(rename('all.min.js'))
        .pipe(uglify())
        .pipe(gulp.dest('js/dist'));
});


// Watch Files For Changes
gulp.task('watch', function() {
    gulp.watch('js/*.js', ['lint', 'scripts']);
    gulp.watch('scss/*.scss', ['sass']);
});


// Minify css files task
gulp.task('minify-css', function() {
  return gulp.src('css/src/*.css')
    .pipe(concat('all.css'))
    .pipe(gulp.dest('css/dist'))
    .pipe(rename('all.min.css'))
    //.pipe(minifyCss({compatibility: 'ie8'}))
    .pipe(minifyCss())
    .pipe(gulp.dest('css/dist'));
});


// Default Task
gulp.task('default', ['lint', 'sass', 'watch']);//scripts
gulp.task('minify', ['minify-js', 'minify-css']);