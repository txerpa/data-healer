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
        if (arr.length % 2 === 0) {
            for (let i = 0; i < arr.length; i += count) {
                chunks.push([arr[i], arr[i + 1]]);
            }
        } else {
            for (let i = 0; i < arr.length - 1; i += count) {
                chunks.push([arr[i], arr[i + 1]]);
            }
            chunks.push([arr[arr.length - 1]]);
        }
        return chunks;
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
            timeout: 30000,
        }).show();
    },

};

window.utils = utils;

String.prototype.replaceAll = function (search, replacement) {
    return this.replace(new RegExp(search, 'g'), replacement);
};
