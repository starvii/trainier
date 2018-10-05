/*

<div class="container">
	<div class="columns" v-for="(option, index) in options" @dblclick="changeAnswer(index)">
		<div class="column is-1">
			<span v-text="`ABCDEFGHIJKL`[index] + `.`"></span>
		</div>
		<div class="column is-5">
			<p class="control has-icons-right">
				<input class="input is-small" type="text" placeholder="English Option"
					   v-model="option.en_option"
					   :class="[option.is_true ? 'is-success' : 'is-danger']">
				<span class="icon is-small is-right">
					<i class="fas fa-check" v-if="option.is_true"></i>
					<i class="fas fa-times" v-if="!option.is_true"></i>
				</span>
			</p>
		</div>
		<div class="column is-5">
			<p class="control has-icons-right">
				<input class="input is-small" type="text" placeholder="Chinese Option"
					   v-model="option.cn_option"
					   :class="[option.is_true ? 'is-success' : 'is-danger']">
				<span class="icon is-small is-right">
					<i class="fas fa-check" v-if="option.is_true"></i>
					<i class="fas fa-times" v-if="!option.is_true"></i>
				</span>
			</p>
		</div>
		<div class="column is-1">
			<div class="buttons has-addons">
				<a class="button is-small" @click="insertOption(index)">
					<i class="fas fa-plus"></i>
				</a>
				<a class="button is-small" @click="removeOption(index)">
					<i class="fas fa-minus"></i>
				</a>
			</div>
		</div>
	</div>
</div>

*/


const OptionsComponent = Vue.extend({
    template: '' +
        '<div class="container">\n' +
        '\t<div class="columns" v-for="(option, index) in options" @dblclick="changeAnswer(index)">\n' +
        '\t\t<div class="column is-1">\n' +
        '\t\t\t<span v-text="`ABCDEFGHIJKL`[index] + `.`"></span>\n' +
        '\t\t</div>\n' +
        '\t\t<div class="column is-5">\n' +
        '\t\t\t<p class="control has-icons-right">\n' +
        '\t\t\t\t<input class="input is-small" type="text" placeholder="English Option"\n' +
        '\t\t\t\t\t   v-model="option.en_option"\n' +
        '\t\t\t\t\t   :class="[option.is_true ? \'is-success\' : \'is-danger\']">\n' +
        '\t\t\t\t<span class="icon is-small is-right">\n' +
        '\t\t\t\t\t<i class="fas fa-check" v-if="option.is_true"></i>\n' +
        '\t\t\t\t\t<i class="fas fa-times" v-if="!option.is_true"></i>\n' +
        '\t\t\t\t</span>\n' +
        '\t\t\t</p>\n' +
        '\t\t</div>\n' +
        '\t\t<div class="column is-5">\n' +
        '\t\t\t<p class="control has-icons-right">\n' +
        '\t\t\t\t<input class="input is-small" type="text" placeholder="Chinese Option"\n' +
        '\t\t\t\t\t   v-model="option.cn_option"\n' +
        '\t\t\t\t\t   :class="[option.is_true ? \'is-success\' : \'is-danger\']">\n' +
        '\t\t\t\t<span class="icon is-small is-right">\n' +
        '\t\t\t\t\t<i class="fas fa-check" v-if="option.is_true"></i>\n' +
        '\t\t\t\t\t<i class="fas fa-times" v-if="!option.is_true"></i>\n' +
        '\t\t\t\t</span>\n' +
        '\t\t\t</p>\n' +
        '\t\t</div>\n' +
        '\t\t<div class="column is-1">\n' +
        '\t\t\t<div class="buttons has-addons">\n' +
        '\t\t\t\t<a class="button is-small" @click="insertOption(index)">\n' +
        '\t\t\t\t\t<i class="fas fa-plus"></i>\n' +
        '\t\t\t\t</a>\n' +
        '\t\t\t\t<a class="button is-small" @click="removeOption(index)">\n' +
        '\t\t\t\t\t<i class="fas fa-minus"></i>\n' +
        '\t\t\t\t</a>\n' +
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