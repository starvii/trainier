const OptionsComponent = Vue.extend({
    template: '' +
        '<div class="columns">\n' +
        '\t<div class="column is-12">\n' +
        '\t\t<div class="columns" v-for="(opt, index) in options" @dblclick="changeAnswer(index)">\n' +
        '\t\t\t<div class="column is-1">\n' +
        '\t\t\t\t<span v-text="`ABCDEFGHIJKL`[index] + `.`"></span>\n' +
        '\t\t\t</div>\n' +
        '\t\t\t<div class="column is-5">\n' +
        '\t\t\t\t<p class="control has-icons-right">\n' +
        '\t\t\t\t\t<input class="input is-small" type="text" placeholder="English Option"\n' +
        '\t\t\t\t\t\t   v-model="opt.en_option"\n' +
        '\t\t\t\t\t\t   :class="[opt.is_true ? \'is-success\' : \'is-danger\']">\n' +
        '\t\t\t\t\t<span class="icon is-small is-right">\n' +
        '\t\t\t\t\t\t<i class="fas fa-check" v-if="opt.is_true"></i>\n' +
        '\t\t\t\t\t\t<i class="fas fa-times" v-if="!opt.is_true"></i>\n' +
        '\t\t\t\t\t</span>\n' +
        '\t\t\t\t</p>\n' +
        '\t\t\t</div>\n' +
        '\t\t\t<div class="column is-5">\n' +
        '\t\t\t\t<p class="control has-icons-right">\n' +
        '\t\t\t\t\t<input class="input is-small" type="text" placeholder="Chinese Option"\n' +
        '\t\t\t\t\t\t   v-model="opt.cn_option"\n' +
        '\t\t\t\t\t\t   :class="[opt.is_true ? \'is-success\' : \'is-danger\']">\n' +
        '\t\t\t\t\t<span class="icon is-small is-right">\n' +
        '\t\t\t\t\t\t<i class="fas fa-check" v-if="opt.is_true"></i>\n' +
        '\t\t\t\t\t\t<i class="fas fa-times" v-if="!opt.is_true"></i>\n' +
        '\t\t\t\t\t</span>\n' +
        '\t\t\t\t</p>\n' +
        '\t\t\t</div>\n' +
        '\t\t\t<div class="column is-1">\n' +
        '\t\t\t\t<div class="buttons has-addons">\n' +
        '\t\t\t\t\t<span class="button is-small" @click="insertOption(index)"><i\n' +
        '\t\t\t\t\t\t\tclass="fas fa-plus"></i></span>\n' +
        '\t\t\t\t\t<span class="button is-small" @click="removeOption(index)"><i\n' +
        '\t\t\t\t\t\t\tclass="fas fa-minus"></i></span>\n' +
        '\t\t\t\t</div>\n' +
        '\t\t\t</div>\n' +
        '\t\t</div>\n' +
        '\t</div>\n' +
        '</div>',
    replace: true,
    props: {
        options: {
            type: Array,
            require: true,
        },
    },
    methods: {
        insertOption: function (idx) {
            if (this.options.length < 12) {
                this.options.splice(idx + 1, 0, {
                    entity_id: '',
                    trunk_id: '',
                    en_option: '',
                    cn_option: '',
                    is_true: false,
                });
            }
        },
        removeOption: function (idx) {
            if (this.options.length > 1) {
                this.options.splice(idx, 1);
            }
        },
        changeAnswer: function (idx) {
            this.options[idx].is_true = !this.options[idx].is_true;
        },
    },
});

Vue.component('options-component', OptionsComponent);