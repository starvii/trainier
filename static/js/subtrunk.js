// sub (child) trunk

/*

<div class="container">
	<div class="columns">
		<div class="column is-12">
			<div class="field">
				<label class="label">英文题目</label>
				<div class="control">
					<div :id="trunkEnId" :name="trunkEnId"></div>
				</div>
			</div>
		</div>
	</div>
	<div class="columns">
		<div class="column is-12">
			<div class="field">
				<label class="label">中文题目</label>
				<div class="control">
					<div :id="trunkCnId" :name="trunkCnId"></div>
				</div>
			</div>
		</div>
	</div>

	<options-component :options.sync="trunk.options"></options-component>
	<div class="container">
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

*/

//import('../ckeditor/classic/ckeditor.js');
//import('./options.js');


const TrunkComponent = Vue.extend({
    template: '' +
        '<div class="container">\n' +
        '\t<div class="columns">\n' +
        '\t\t<div class="column is-12">\n' +
        '\t\t\t<div class="field">\n' +
        '\t\t\t\t<label class="label">英文题目</label>\n' +
        '\t\t\t\t<div class="control">\n' +
        '\t\t\t\t\t<div :id="trunkEnId" :name="trunkEnId"></div>\n' +
        '\t\t\t\t</div>\n' +
        '\t\t\t</div>\n' +
        '\t\t</div>\n' +
        '\t</div>\n' +
        '\t<div class="columns">\n' +
        '\t\t<div class="column is-12">\n' +
        '\t\t\t<div class="field">\n' +
        '\t\t\t\t<label class="label">中文题目</label>\n' +
        '\t\t\t\t<div class="control">\n' +
        '\t\t\t\t\t<div :id="trunkCnId" :name="trunkCnId"></div>\n' +
        '\t\t\t\t</div>\n' +
        '\t\t\t</div>\n' +
        '\t\t</div>\n' +
        '\t</div>\n' +
        '\t\n' +
        '\t<options-component :options.sync="trunk.options"></options-component>\n' +
        '\t<div class="container">\n' +
        '\t\t<div class="field">\n' +
        '\t\t\t<div class="field-body">\n' +
        '\t\t\t\t<div class="field">\n' +
        '\t\t\t\t\t<p class="control is-expanded">\n' +
        '\t\t\t\t\t\t<textarea rows="2" class="textarea is-small" placeholder="analysis"\n' +
        '\t\t\t\t\t\t\t\t  v-model="trunk.analysis"></textarea>\n' +
        '\t\t\t\t\t</p>\n' +
        '\t\t\t\t</div>\n' +
        '\t\t\t\t<div class="field">\n' +
        '\t\t\t\t\t<p class="control is-expanded">\n' +
        '\t\t\t\t\t\t<textarea rows="2" class="textarea is-small" placeholder="comment"\n' +
        '\t\t\t\t\t\t\t\t  v-model="trunk.comment"></textarea>\n' +
        '\t\t\t\t\t</p>\n' +
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
    created: function () {

    },
    data: function () {
        return {
            trunkEnId: 'trunk-en-',
            trunkCnId: 'trunk-cn-',
            trunkEnEditor: null,
            trunkCnEditor: null,
        };
    },
    mounted: function () {
        let suffix = Math.random().toString().substr(2);
        this['trunkEnId'] = 'trunk-en-' + suffix;
        this['trunkCnId'] = 'trunk-cn-' + suffix;
        if (typeof this.trunk === 'undefined' || this.trunk === null) {
            this.trunk = {
                en_trunk: '',
                cn_trunk: '',
                options: [
                    {
                        entity_id: '',
                        trunk_id: '',
                        en_option: '',
                        cn_option: '',
                        is_true: false,
                        order_num: 0,
                        comment: '',
                    },
                    {
                        entity_id: '',
                        trunk_id: '',
                        en_option: '',
                        cn_option: '',
                        is_true: false,
                        order_num: 0,
                        comment: '',
                    },
                    {
                        entity_id: '',
                        trunk_id: '',
                        en_option: '',
                        cn_option: '',
                        is_true: false,
                        order_num: 0,
                        comment: '',
                    },
                    {
                        entity_id: '',
                        trunk_id: '',
                        en_option: '',
                        cn_option: '',
                        is_true: false,
                        order_num: 0,
                        comment: '',
                    },
                ],
                analysis: '',
                comment: '',
            };
        }
        ClassicEditor
            .create(document.querySelector(`div[name=${this.trunkEnId}`), {
                toolbar: ['imageUpload'],
                ckfinder: {
                    uploadUrl: '/upload/',
                },
            })
            .then(editor => {
                console.debug(editor);
                app.trunkEnEditor = editor;
                app.trunkEnEditor.setData('123');
                //app.trunkEnEditor.setData(this.trunk.en_trunk);
            })
            .catch(error => {
                alert(error);
            });
        ClassicEditor
            .create(document.querySelector(`div[name=${this.trunkCnId}]`), {
                toolbar: ['imageUpload'],
                ckfinder: {
                    uploadUrl: '/upload/',
                },
            })
            .then(editor => {
                app.trunkCnCditor = editor;
                //app.trunkCnEditor.setData(this.trunk.cn_trunk);
                app.trunkCnEditor.setData('123');
            })
            .catch(error => {
                alert(error);
            });
    },
    methods: {

    },
});

Vue.component('trunk-component', TrunkComponent);