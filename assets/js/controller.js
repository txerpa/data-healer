/* eslint-disable camelcase,no-trailing-spaces,no-undef,no-prototype-builtins,no-restricted-syntax,no-plusplus,no-unused-vars,guard-for-in,no-const-assign */

/*
    Controller data-healer
*/

const controller = new Vue({

    el: '#app',

    data: {

        // Configuration  (conf.py) Only for show
        separator: '',
        input_file: '',
        columns_to_show: '',
        help_column: '',
        output_file: '',
        output_file_exists: false,
        inferred_column: '',

        categories: [],

        // Current row in the CSV
        n_row: 0,
        row: {},
        total_rows: 0,
    },

    computed: {

        /**
         * Computable for show the dataset progress
         * @returns {string}
         */
        progress() {
            return `${this.n_row} of ${this.total_rows}`;
        },

        /**
         * Computable that shows dynamic categories in categories HTML card
         * @returns {html}
         */
        categorySections() {
            return utils.chunkArray(this.categories, 2);
        },
    },

    methods: {

        /**
         * Controller init function
         * @param separator: CSV separator
         * @param input_file: Dataset input file
         * @param columns_to_show: Dataset columns to show the user
         * @param help_column: If not null is a clue for the user
         * @param output_file: Dataset output file
         * @param output_file_exists: There is an existing output file
         * @param inferred_column: Column name of the inferred column
         */
        init(separator, input_file, columns_to_show, help_column,
             output_file, output_file_exists, inferred_column) {
            this.separator = separator;
            this.input_file = input_file;
            this.columns_to_show = utils.strToList(columns_to_show);
            this.help_column = help_column;
            this.output_file = output_file;
            this.output_file_exists = output_file_exists === '1';
            this.inferred_column = inferred_column;

            if (this.output_file_exists) {
                utils.showNoty('It seems that there is an output file started. You will continue categorizing ' +
                               'that file. If you want to start over from the beginning you have to move or drop' +
                               ' the current output file.', 'success');
            }
        },

        /**
         * Function that checks the configurations
         */
        check_confs() {
            this.$http.get('/check_confs/').then((response) => {
                if (response.body.errors.length === 0) {
                    utils.showNoty('Start!', 'success');
                    document.querySelector('#summary-card').style.display = 'none';
                    document.querySelector('#app-card').style.display = 'block';
                    this.getRow();
                    this.getCategories();
                } else {
                    for (let i = 0; i < response.body.errors.length; i++) {
                        utils.showNoty(response.body.errors[i], 'error');
                    }
                }
            }, (response) => {
                utils.showNoty(response.body, 'error');
            });
        },

        /**
         * Function that makes an AJAX request to the server to obtain the next row of the dataset
         */
        getRow() {
            const url = `/get_row/?n_row=${String(this.n_row)}`;
            this.$http.get(url).then((response) => {
                this.row = response.body.row;
                this.n_row = response.body.n_row;
            }, (response) => {
                utils.showNoty(response.body, 'error');
            });
        },

        /**
         * Function that obtains the available categories for classify a row
         */
        getCategories() {
            this.$http.get('/get_categories/').then((response) => {
                this.categories = response.body.categories;
                this.total_rows = response.body.total_rows;
            }, (response) => {
                utils.showNoty(response.body, 'error');
            });
        },

        /**
         * Function that posts a new row in the result dataset
         */
        postRow(event) {
            const category = $(event.target).text().replace(/\s/g, '');
            this.$http.post('/post_row/', { n_row: this.n_row, category }).then(() => {
                this.nextRow();
            }, (response) => {
                utils.showNoty(response.body, 'error');
            });
        },

        /**
         * Function that gets the CSV next row
         */
        nextRow() {
            this.n_row += 1;
            this.getRow();
        },
    },
});

window.controller = controller;
