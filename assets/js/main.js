/* eslint-disable import/newline-after-import */

/*
 * Main Javascript file for data-healer.
 *
 * This file bundles all of your javascript together using webpack.
 */

import VueResource from 'vue-resource';
import PNotify from 'pnotify';

// JavaScript modules
require('jquery');
require('font-awesome-webpack');
require('bootstrap');
require('materialize-css');

/* Global variables definition */

// Vue
const Vue = require('vue');
Vue.use(VueResource);
Vue.config.devtools = true;
window.Vue = Vue;

// Pnotify
PNotify.prototype.options.styling = 'fontawesome';
window.PNotify = PNotify;

// Own code
require('./utils.js');
require('./controller.js');
