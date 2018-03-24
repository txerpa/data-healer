/* eslint-disable camelcase,no-trailing-spaces,no-undef,no-prototype-builtins,no-restricted-syntax,no-plusplus,no-unused-vars,guard-for-in,no-const-assign,radix */

/*
 * Data-healer controller
 */

const controller = new Vue({

    el: '#app',

    data: {

        // Configuration
        input_file: '',
        separator: 'semicolon',
        columns_to_show: '',
        default_column: '',
        output_file: '',
        class_column: '',
        classes: '',

        // Current row in the CSV
        n_row: 0,
        row: {},
        total_rows: 0,

        // Modal input text value
        new_class: '',
    },

    mounted() {
        $('.modal').modal();
    },

    watch: {

        /**
         * Function called after update row which calculates materialize textarea heights
         */
        row() {
            // nextTick() waits until Vue render process is finished
            Vue.nextTick(() => {
                const textareas = $('.materialize-textarea');
                for (let i = 0, len = textareas.length; i < len; i++) {
                    const textarea = $(textareas[i]);
                    const content = textarea.val();
                    const line_height = parseInt(textarea.css('line-height').split('px')[0]);
                    const n_rows = (content.match(/\n/g) || []).length;
                    textarea.css('height', line_height * n_rows);
                }
            });
        },
    },

    computed: {

        /**
         * Computable for show the dataset progress
         * @returns {string}
         */
        progress() {
            return `${this.n_row} of ${this.total_rows}`;
        },

    },

    methods: {

        /**
         * Function that makes an AJAX request
         * for check the configurations set by the user
         */
        start() {
            const data = {
                input_file: this.input_file,
                separator: this.separator,
                columns_to_show: this.columns_to_show,
                default_column: this.default_column,
                output_file: this.output_file,
                class_column: this.class_column,
                classes: this.classes,
            };
            this.$http.post('/start/', data).then((response) => {
                if (!response.body.hasOwnProperty('errors')) {
                    utils.showNoty('Start!', 'success');
                    document.querySelector('#config-card').style.display = 'none';
                    document.querySelector('#progress').style.display = 'block';
                    document.querySelector('#configuration').style.display = 'block';
                    document.querySelector('#app-card').style.display = 'block';
                    this.classes = response.body.classes;
                    this.total_rows = response.body.total_rows;
                    this.getRow();
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
         * Function that makes an AJAX request to
         * obtain the n specified row of the dataset
         */
        getRow() {
            const url = `/get_row/?input_file=${this.input_file}&separator=${this.separator}
            &columns_to_show=${this.columns_to_show}&default_column=${this.default_column}
            &output_file=${this.output_file}&class_column=${this.class_column}&n_row=${this.n_row}`;
            this.$http.get(url).then((response) => {
                if (response.body.finish === 1) {
                    utils.showNoty('Finish!', 'success');
                    document.querySelector('#app-card').style.display = 'none';
                    document.querySelector('#finish-card').style.display = 'block';
                } else {
                    if (response.body.existing_control_file === 1) {
                        utils.showNoty('There is a control file saved, you will continue with it. \n' +
                            'If you want to start again, specify a new output file in the configuration form', 'info');
                    }
                    this.row = response.body.row;
                    this.n_row = response.body.n_row;
                }
            }, (response) => {
                utils.showNoty(response.body, 'error');
            });
        },

        /**
         * Function that makes an AJAX request to save a new
         * categorized row in the result dataset
         */
        saveRow(event) {
            const data = {
                input_file: this.input_file,
                separator: this.separator,
                output_file: this.output_file,
                class_column: this.class_column,
                n_row: this.n_row,
                row: this.row,
                selected_class: $(event.target).text().trim(),
            };
            this.$http.post('/save_row/', data).then(() => {
                this.getNextRow();
            }, (response) => {
                utils.showNoty(response.body, 'error');
            });
        },

        /**
         * Function that gets next CSV row
         */
        getNextRow() {
            this.n_row += 1;
            this.getRow();
        },

        /**
         * Function that makes an AJAX request to
         * recover the last row passed
         */
        getPreviousRow() {
            this.n_row -= 1;
            const url = `/get_previous_row/?input_file=${this.input_file}&separator=${this.separator}
            &columns_to_show=${this.columns_to_show}&default_column=${this.default_column}
            &output_file=${this.output_file}&class_column=${this.class_column}&n_row=${this.n_row}`;
            this.$http.get(url).then((response) => {
                this.row = response.body.row;
                this.n_row = response.body.n_row;
            }, (response) => {
                utils.showNoty(response.body, 'error');
            });
        },

        /**
         * Function that adds the specified new class to the classes array
         */
        addClass() {
            if (this.classes.indexOf(this.new_class) >= 0) {
                utils.showNoty('This class already exists', 'error');
            } else {
                this.classes.push(this.new_class);
                $('#modal-new-class').modal('close');
            }
            this.new_class = '';
        },

    },
});


window.controller = controller;
