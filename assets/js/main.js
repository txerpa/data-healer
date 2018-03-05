/* eslint-disable import/newline-after-import */
/*
 * Main Javascript file for data-healer.
 *
 * This file bundles all of your javascript together using webpack.
 */

// JavaScript modules
require('jquery');
require('font-awesome-webpack');
require('materialize-css');

const Vue = require('vue');
Vue.config.devtools = true;
window.Vue = Vue;

// Your own code
require('./utils.js');
require('./controller.js');
