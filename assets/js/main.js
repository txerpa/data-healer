/* eslint-disable import/newline-after-import */

/*
 * Main Javascript file for data-healer.
 *
 * This file bundles all of your javascript together using webpack.
 */

import VueResource from 'vue-resource';

// JavaScript modules
require('font-awesome-webpack');
require('materialize-css');

/* Global variables definition */

// Vue
const Vue = require('vue');
Vue.use(VueResource);
Vue.config.devtools = true;
window.Vue = Vue;

// Notifications
const Noty = require('noty');
window.Noty = Noty;

// Own code
require('./utils.js');
require('./controller.js');
