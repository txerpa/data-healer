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
         * Function called when the user clicks the start button
         */
        start() {
            console.log('Start');
        },
    },

});

window.controller = controller;
