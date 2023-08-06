'use strict';

var gulp = require('gulp'),
    sass = require('gulp-sass'),
    paths = {
        'input': {
            'sass': './formed/private/scss/**/*.scss'
        },
        'output': {
            'css': './formed/static/admin/form_definition/css'
        }
    };

function swallowError (error) {
    //If you want details of the error in the console
    console.log(error.toString());

    this.emit('end');
}

/**
 * Compiles sass files
 * @see https://github.com/sass/node-sass#options
 */
gulp.task('sass', function () {
    gulp.src(paths.input.sass)
        .pipe(sass({
            'outputStyle': 'compressed'
        }).on('error', swallowError))
        .pipe(gulp.dest(paths.output.css));
});

/**
 * Simple build all, compiles sass.
 */
gulp.task('build', ['sass']);

/**
 * Watches file changes and call tasks
 */
gulp.task('watch', function () {
    gulp.watch(paths.input.sass, ['sass']);
});

/**
 * Build all, then watch
 */
gulp.task('default', ['build', 'watch']);
