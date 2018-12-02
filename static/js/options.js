/*

<div>
	<div class="form-row justify-content-between" v-if="options.length<=0">
		<label class="float-left">选项</label>
		<a class="btn btn-sm" href="javascript:void(0);" @click="insertOption(-1)">
			<i class="fas fa-plus"></i>
		</a>
	</div>
	<div class="form-row pb-2" v-else v-for="(option, index) in options" @dblclick="changeAnswer(index)">
		<div class="col justify-content-between">
			<span @click="changeAnswer(index)">
				<i class="fas fa-check-circle text-success" v-if="option.is_true"></i>
				<i class="fas fa-times-circle text-danger" v-else></i>
			</span>
			<label class="float-right" v-text="`ABCDEFGHIJKL`[index] + `.`"></label>
		</div>
		<div class="col-5">
			<input class="form-control form-control-sm" type="text" placeholder="English Option"
				v-model="option.en_option"
				:class="[option.is_true?'is-valid':'is-invalid']">
		</div>
		<div class="col-5">
			<input class="form-control form-control-sm" type="text" placeholder="中文选项"
				v-model="option.cn_option"
				:class="[option.is_true?'is-valid':'is-invalid']">
		</div>
		<div class="col justify-content-end">
			<div class="btn-group">
				<a class="btn btn-sm" href="javascript:void(0);" @click="insertOption(index)">
					<i class="fas fa-plus"></i>
				</a>
				<a class="btn btn-sm" href="javascript:void(0);" @click="removeOption(index)">
					<i class="fas fa-minus"></i>
				</a>
			</div>
		</div>
	</div>
</div>

*/


const OptionsComponent = Vue.extend({
    template: '' +
        '<div>\n' +
        '\t<div class="form-row justify-content-between" v-if="options.length<=0">\n' +
        '\t\t<label class="float-left">选项</label>\n' +
        '\t\t<a class="btn btn-sm" href="javascript:void(0);" @click="insertOption(-1)">\n' +
        '\t\t\t<i class="fas fa-plus"></i>\n' +
        '\t\t</a>\n' +
        '\t</div>\n' +
        '\t<div class="form-row pb-2" v-else v-for="(option, index) in options" @dblclick="changeAnswer(index)">\n' +
        '\t\t<div class="col justify-content-between">\n' +
        '\t\t\t<span @click="changeAnswer(index)">\n' +
        '\t\t\t\t<i class="fas fa-check-circle text-success" v-if="option.is_true"></i>\n' +
        '\t\t\t\t<i class="fas fa-times-circle text-danger" v-else></i>\n' +
        '\t\t\t</span>\n' +
        '\t\t\t<label class="float-right" v-text="`ABCDEFGHIJKL`[index] + `.`"></label>\n' +
        '\t\t</div>\n' +
        '\t\t<div class="col-5">\n' +
        '\t\t\t<input class="form-control form-control-sm" type="text" placeholder="English Option"\n' +
        '\t\t\t\tv-model="option.en_option"\n' +
        '\t\t\t\t:class="[option.is_true?\'is-valid\':\'is-invalid\']">\n' +
        '\t\t</div>\n' +
        '\t\t<div class="col-5">\n' +
        '\t\t\t<input class="form-control form-control-sm" type="text" placeholder="中文选项"\n' +
        '\t\t\t\tv-model="option.cn_option"\n' +
        '\t\t\t\t:class="[option.is_true?\'is-valid\':\'is-invalid\']">\n' +
        '\t\t</div>\n' +
        '\t\t<div class="col justify-content-end">\n' +
        '\t\t\t<div class="btn-group">\n' +
        '\t\t\t\t<a class="btn btn-sm" href="javascript:void(0);" @click="insertOption(index)">\n' +
        '\t\t\t\t\t<i class="fas fa-plus"></i>\n' +
        '\t\t\t\t</a>\n' +
        '\t\t\t\t<a class="btn btn-sm" href="javascript:void(0);" @click="removeOption(index)">\n' +
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
                this.options.splice(idx + 1, 0, newOption());
            }
        },
        removeOption: function (idx) {
            if (this.options.length >= 0) {
                this.options.splice(idx, 1);
            }
        },
        changeAnswer: function (idx) {
            this.options[idx].is_true = !this.options[idx].is_true;
        },
    },
});

Vue.component('options-component', OptionsComponent);
