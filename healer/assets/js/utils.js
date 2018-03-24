/* eslint-disable no-extend-native,guard-for-in,func-names,no-plusplus,no-prototype-builtins,no-restricted-syntax,no-undef */

/*
 * Util functions
 */

const utils = {

    /**
     * Function that preprocess a list serialized as a string
     * @param {str} str
     * @returns {array}
     */
    strToList(str) {
        let result = str.slice(1, -1);
        result = result.replaceAll(/\s/g, '');
        result = result.replaceAll('&#39;', '');
        return result.split(',');
    },

    /**
     * Function that shows an error notification
     * @param {str} text
     * @param {str} type (warning, error, success)
     */
    showNoty(text, type) {
        new Noty({
            type,
            text,
            layout: 'topRight',
            theme: 'sunset',
            timeout: 15000,
        }).show();
    },

};

window.utils = utils;

String.prototype.replaceAll = function (search, replacement) {
    return this.replace(new RegExp(search, 'g'), replacement);
};

String.prototype.trim = function () {
    return this.toString().replace(/^\s+|\s+$/g, '');
};
