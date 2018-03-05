/* eslint-disable camelcase,no-trailing-spaces,no-undef */

/*
    Controller data-healer
*/

const controller = new Vue({

    el: '#app',

    data: {
        input_file: '',
        input_separator: '',
        columns_to_show: '',
        help_column: '',
        output_file: '',
        output_separator: '',
        inferred_column: '',

        row: 0,
    },

    computed: {

    },

    methods: {

        /**
         * Controller init function
         * @param input_file: Dataset input file
         * @param input_separator: CSV input separator
         * @param columns_to_show: Dataset columns to show the user
         * @param help_column: If not null is a clue for the user
         * @param output_file: Dataset output file
         * @param output_separator: CSV output separator
         * @param inferred_column: Column name of the inferred column
         */
        init(input_file, input_separator, columns_to_show,
             help_column, output_file, output_separator, inferred_column) {
            this.input_file = input_file;
            this.input_separator = input_separator;
            this.columns_to_show = utils.strToList(columns_to_show);
            this.help_column = help_column;
            this.output_file = output_file;
            this.output_separator = output_separator;
            this.inferred_column = inferred_column;
        },

        /**
         * Function that makes an AJAX request to the server to obtain the next row of the dataset
         * @param {int} row
         */
        get_row(row = 0) {
            const url = `/get_row/?row=${String(row)}`;
            this.$http.get(url).then((response) => {
                console.log(response.body);
            }, () => {
                console.log('Show error');
            });
        },

        /**
         * Function called when the user clicks the start button
         */
        start() {
            $('#summary-card').css('display', 'none');
            $('#app-card').css('display', 'block');
            this.get_row();
        },
    },

});

window.controller = controller;
