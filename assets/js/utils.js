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
     * Function that cast a list into a string for show in the HTML
     * @param {array} list
     */
    listToStr(list) {
        return Array(list).join(', ');
    },

    /**
     * Chunk an array in groups of count size
     * @param {array} arr
     * @param {int} count
     * @returns {array}
     */
    chunkArray(arr, count) {
        const chunks = [];
        while (arr.length) {
            const chunkSize = Math.ceil(arr.length / count--);
            const chunk = arr.slice(0, chunkSize);
            chunks.push(chunk);
            arr = arr.slice(chunkSize);
        }
        return chunks;
    },

    /**
     * Function that shows an error notification
     * @param {str} text
     */
    showError(text) {
        new Noty({
            type: 'error',
            layout: 'topRight',
            theme: 'sunset',
            text,
        }).show();
    },

    /**
     * Function that shows a success notification
     * @param {str} text
     */
    showSuccess(text) {
        new Noty({
            type: 'success',
            layout: 'topRight',
            theme: 'sunset',
            text,
        }).show();
    },

};

window.utils = utils;

String.prototype.replaceAll = function (search, replacement) {
    return this.replace(new RegExp(search, 'g'), replacement);
};
