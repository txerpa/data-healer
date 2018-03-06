/* eslint-disable camelcase,no-trailing-spaces,no-undef,no-prototype-builtins,no-restricted-syntax,no-plusplus,no-unused-vars,guard-for-in,no-const-assign */

/*
    Controller data-healer
*/

const controller = new Vue({

    el: '#app',

    data: {

        // Configuration  (conf.py) Only for show
        input_file: '',
        input_separator: '',
        columns_to_show: '',
        help_column: '',
        output_file: '',
        output_separator: '',
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
         * Computable that shows dynamic row attrs in content HTML card
         * @returns {html}
         */
        showRow() {
            let html = '<ul class="collection">';
            for (const key in this.row) {
                if (this.row.hasOwnProperty(key)) {
                    html += `<li class="collection-item">${this.row[key]}</li>`;
                }
            }
            html += '</ul>';
            return html;
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
         * Function that checks the configurations
         */
        check_confs() {
            this.$http.get('/check_confs/').then((response) => {
                if (response.body.errors.length === 0) {
                    utils.showSuccess('Start!');
                    $('#summary-card').css('display', 'none');
                    $('#app-card').css('display', 'block');
                    this.getRow();
                    this.getCategories();
                } else {
                    for (let i = 0; i < response.body.errors.length; i++) {
                        utils.showError(response.body.errors[i]);
                    }
                }
            }, (response) => {
                utils.showError(response.body);
            });
        },

        /**
         * Function that makes an AJAX request to the server to obtain the next row of the dataset
         */
        getRow() {
            const url = `/get_row/?row=${String(this.n_row)}`;
            this.$http.get(url).then((response) => {
                this.row = response.body.row;
            }, (response) => {
                utils.showError(response.body);
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
                utils.showError(response.body);
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
                utils.showError(response.body);
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
