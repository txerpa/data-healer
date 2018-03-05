/* eslint-disable no-extend-native,guard-for-in,func-names */
/*
 * Util functions
 */

const utils = {

    /**
     * Function that preprocess a list serialized as a string
     * @param str
     * @returns {array}
     */
    strToList(str) {
        let result = str.slice(1, -1);
        result = result.replaceAll(/\s/g, '');
        result = result.replaceAll('&#39;', '');
        return result.split(',');
    },

    /**
     * Function that cast a list into a string for show in the HTML
     * @param list
     */
    listToStr(list) {
        return Array(list).join(', ');
    },
};

window.utils = utils;

String.prototype.replaceAll = function (search, replacement) {
    return this.replace(new RegExp(search, 'g'), replacement);
};
