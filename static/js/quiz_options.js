/*

<div class="container">
	<label v-for="(option, index) in options" :for="prefix + `ABCDEFGHIJKL`[index]">
		<div class="columns">
			<div class="column is-1">
				<input :id="prefix + `ABCDEFGHIJKL`[index]" type="checkbox"
					:name="prefix + `answer`" :value="`ABCDEFGHIJKL`[index]"
					v-model="question.a"
					v-if="option.multi_choice">
				<input :id="prefix + `ABCDEFGHIJKL`[index]" type="radio"
					:name="prefix + `answer`" :value="`ABCDEFGHIJKL`[index]"
					v-model="question.a"
					v-else>
				<span v-text="`ABCDEFGHIJKL`[index] + `.`"></span>
			</div>
			<div class="column is-5" v-if="option.en_option.length>0&&option.cn_option.length>0">
				<pre v-text="option.en_option"></pre>
			</div>
			<div class="column is-5" v-if="option.en_option.length>0&&option.cn_option.length>0">
				<pre v-text="option.cn_option"></pre>
			</div>
			<div class="column is-1" v-if="option.en_option.length>0&&option.cn_option.length>0">&nbsp;</div>
			<div class="column is-11" v-else>
				<pre v-text="option.x_option"></pre>
			</div>
		</div>
	</label>
</div>

*/


const QuizOptionsComponent = Vue.extend({
    template: '' +
        '<div class="container">\n' +
        '\t<label v-for="(option, index) in options" :for="prefix + `ABCDEFGHIJKL`[index]">\n' +
        '\t\t<div class="columns">\n' +
        '\t\t\t<div class="column is-1">\n' +
        '\t\t\t\t<input :id="prefix + `ABCDEFGHIJKL`[index]" type="checkbox"\n' +
        '\t\t\t\t\t:name="prefix + `answer`" :value="`ABCDEFGHIJKL`[index]"\n' +
        '\t\t\t\t\tv-model="question.a"\n' +
        '\t\t\t\t\tv-if="option.multi_choice">\n' +
        '\t\t\t\t<input :id="prefix + `ABCDEFGHIJKL`[index]" type="radio"\n' +
        '\t\t\t\t\t:name="prefix + `answer`" :value="`ABCDEFGHIJKL`[index]"\n' +
        '\t\t\t\t\tv-model="question.a"\n' +
        '\t\t\t\t\tv-else>\n' +
        '\t\t\t\t<span v-text="`ABCDEFGHIJKL`[index] + `.`"></span>\n' +
        '\t\t\t</div>\n' +
        '\t\t\t<div class="column is-5" v-if="option.en_option.length>0&&option.cn_option.length>0">\n' +
        '\t\t\t\t<pre v-text="option.en_option"></pre>\n' +
        '\t\t\t</div>\n' +
        '\t\t\t<div class="column is-5" v-if="option.en_option.length>0&&option.cn_option.length>0">\n' +
        '\t\t\t\t<pre v-text="option.cn_option"></pre>\n' +
        '\t\t\t</div>\n' +
        '\t\t\t<div class="column is-1" v-if="option.en_option.length>0&&option.cn_option.length>0">&nbsp;</div>\n' +
        '\t\t\t<div class="column is-11" v-else>\n' +
        '\t\t\t\t<pre v-text="option.x_option"></pre>\n' +
        '\t\t\t</div>\n' +
        '\t\t</div>\n' +
        '\t</label>\n' +
        '</div>',
    replace: true,
    props: {
        prefix: {
            type: String,
            require: true,
        },
        options: {
            type: Array,
            require: true,
        },
        question: {
            type: Object,
            require: true,
        },
    },
    methods: {
    },
});

Vue.component('quiz-options-component', QuizOptionsComponent);