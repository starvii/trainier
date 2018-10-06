// sub (child) trunk

/*

<div class="container">
	<div class="columns">
		<div class="column is-12">
			<div class="field">
				<label class="label">英文题目</label>
				<div class="control">
					<ckeditor type="classic" v-model="trunk.en_trunk" :config="config" :upload-adapter="uploadAdapter"></ckeditor>
				</div>
			</div>
		</div>
	</div>
	<div class="columns">
		<div class="column is-12">
			<div class="field">
				<label class="label">中文题目</label>
				<div class="control">
					<ckeditor type="classic" v-model="trunk.cn_trunk" :config="config" :upload-adapter="uploadAdapter"></ckeditor>
				</div>
			</div>
		</div>
	</div>
	<div class="columns">
		<div class="column is-12">
			<options-component :options.sync="trunk.options"></options-component>
		</div>
	</div>
	<div class="columns">
		<div class="column is-12">
			<div class="field">
				<div class="field-body">
					<div class="field">
						<p class="control is-expanded">
							<textarea rows="2" class="textarea is-small" placeholder="analysis"
									  v-model="trunk.analysis"></textarea>
						</p>
					</div>
					<div class="field">
						<p class="control is-expanded">
							<textarea rows="2" class="textarea is-small" placeholder="comment"
									  v-model="trunk.comment"></textarea>
						</p>
					</div>
				</div>
			</div>
		</div>
	</div>
</div>

*/

const TrunkComponent = Vue.extend({
    template: '' +
        '<div class="container">\n' +
        '\t<div class="columns">\n' +
        '\t\t<div class="column is-12">\n' +
        '\t\t\t<div class="field">\n' +
        '\t\t\t\t<label class="label">英文题目</label>\n' +
        '\t\t\t\t<div class="control">\n' +
        '\t\t\t\t\t<ckeditor type="classic" v-model="trunk.en_trunk" :config="config" :upload-adapter="uploadAdapter"></ckeditor>\n' +
        '\t\t\t\t</div>\n' +
        '\t\t\t</div>\n' +
        '\t\t</div>\n' +
        '\t</div>\n' +
        '\t<div class="columns">\n' +
        '\t\t<div class="column is-12">\n' +
        '\t\t\t<div class="field">\n' +
        '\t\t\t\t<label class="label">中文题目</label>\n' +
        '\t\t\t\t<div class="control">\n' +
        '\t\t\t\t\t<ckeditor type="classic" v-model="trunk.cn_trunk" :config="config" :upload-adapter="uploadAdapter"></ckeditor>\n' +
        '\t\t\t\t</div>\n' +
        '\t\t\t</div>\n' +
        '\t\t</div>\n' +
        '\t</div>\n' +
        '\t<div class="columns">\n' +
        '\t\t<div class="column is-12">\n' +
        '\t\t\t<options-component :options.sync="trunk.options"></options-component>\n' +
        '\t\t</div>\n' +
        '\t</div>\n' +
        '\t<div class="columns">\n' +
        '\t\t<div class="column is-12">\n' +
        '\t\t\t<div class="field">\n' +
        '\t\t\t\t<div class="field-body">\n' +
        '\t\t\t\t\t<div class="field">\n' +
        '\t\t\t\t\t\t<p class="control is-expanded">\n' +
        '\t\t\t\t\t\t\t<textarea rows="2" class="textarea is-small" placeholder="analysis"\n' +
        '\t\t\t\t\t\t\t\t\t  v-model="trunk.analysis"></textarea>\n' +
        '\t\t\t\t\t\t</p>\n' +
        '\t\t\t\t\t</div>\n' +
        '\t\t\t\t\t<div class="field">\n' +
        '\t\t\t\t\t\t<p class="control is-expanded">\n' +
        '\t\t\t\t\t\t\t<textarea rows="2" class="textarea is-small" placeholder="comment"\n' +
        '\t\t\t\t\t\t\t\t\t  v-model="trunk.comment"></textarea>\n' +
        '\t\t\t\t\t\t</p>\n' +
        '\t\t\t\t\t</div>\n' +
        '\t\t\t\t</div>\n' +
        '\t\t\t</div>\n' +
        '\t\t</div>\n' +
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