'use strict';

var gulp = require('gulp'),
	sass = require('gulp-sass');

gulp.task('sass', function () {
	gulp.src('./sass/**/*.scss')
		.pipe(sass())
		.pipe(gulp.dest('./assets/base/css/'));
});

gulp.task('sass:watch', function () {
	gulp.watch('./sass/**/*.scss', ['sass']);
});

var prettify = require('gulp-prettify');
 
gulp.task('prettify', function() {
  gulp.src('../../master/release/theme/*.html')
    .pipe(prettify({
    	indent_size: 4, 
    	indent_inner_html: true,
    	unformatted: ['pre', 'code']
   	}))
    .pipe(gulp.dest('../../master/release/theme/'))
});