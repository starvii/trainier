// sub (child) trunk

/*

<div>
	<div class="form-group">
		<label>英文题目</label>
		<ckeditor type="classic" v-model="trunk.en_trunk" :config="config"
			:upload-adapter="uploadAdapter"></ckeditor>
	</div>
	<div class="form-group">
		<label>中文题目</label>
		<ckeditor type="classic" v-model="trunk.cn_trunk" :config="config"
			:upload-adapter="uploadAdapter"></ckeditor>
	</div>
	<options-component :options.sync="trunk.options"></options-component>
	<div class="form-row">
			<div class="col">
				<label>详解</label>
				<textarea class="form-control form-control-sm" rows="3" v-model="trunk.explanation"></textarea>
			</div>
		<div class="col">
				<label>备注</label>
				<textarea class="form-control form-control-sm" rows="3" v-model="trunk.comment"></textarea>
			</div>
	</div>
</div>

*/

const TrunkComponent = Vue.extend({
    template: '' +
        '<div>\n' +
        '\t<div class="form-group">\n' +
        '\t\t<label>英文题目</label>\n' +
        '\t\t<ckeditor type="classic" v-model="trunk.en_trunk" :config="config"\n' +
        '\t\t\t:upload-adapter="uploadAdapter"></ckeditor>\n' +
        '\t</div>\n' +
        '\t<div class="form-group">\n' +
        '\t\t<label>中文题目</label>\n' +
        '\t\t<ckeditor type="classic" v-model="trunk.cn_trunk" :config="config"\n' +
        '\t\t\t:upload-adapter="uploadAdapter"></ckeditor>\n' +
        '\t</div>\n' +
        '\t<options-component :options.sync="trunk.options"></options-component>\n' +
        '\t<div class="form-row">\n' +
        '\t\t\t<div class="col">\n' +
        '\t\t\t\t<label>详解</label>\n' +
        '\t\t\t\t<textarea class="form-control form-control-sm" rows="3" v-model="trunk.explanation"></textarea>\n' +
        '\t\t\t</div>\n' +
        '\t\t<div class="col">\n' +
        '\t\t\t\t<label>备注</label>\n' +
        '\t\t\t\t<textarea class="form-control form-control-sm" rows="3" v-model="trunk.comment"></textarea>\n' +
        '\t\t\t</div>\n' +
        '\t</div>\n' +
        '</div>',
    replace: true,
    props: {
        trunk: {
            type: Object,
            require: true,
        },
    },
    data: function () {
        return {
            config: ckeditorConfig,
            uploadAdapter: CkeditorUploadAdapter,
        }
    },
    mounted: function () {
    },
    methods: {

    },
});

Vue.component('trunk-component', TrunkComponent);