/*

<div>
	<div class="form-row" v-for="(option, index) in options" :for="prefix + `ABCDEFGHIJKL`[index]">
		<div class="col">
			<input :id="prefix + `ABCDEFGHIJKL`[index]" type="checkbox"
				:name="prefix + `answer`" :value="`ABCDEFGHIJKL`[index]"
				v-model="answer"
				v-if="option.multi_choice">
			<input :id="prefix + `ABCDEFGHIJKL`[index]" type="radio"
				:name="prefix + `answer`" :value="`ABCDEFGHIJKL`[index]"
				v-model="answer"
				v-else>
			<span v-text="`ABCDEFGHIJKL`[index] + `.`"></span>
		</div>
		<div class="col-5" v-if="option.en_option.length>0&&option.cn_option.length>0">
			<pre v-text="option.en_option"></pre>
		</div>
		<div class="col-5" v-if="option.en_option.length>0&&option.cn_option.length>0">
			<pre v-text="option.cn_option"></pre>
		</div>
		<div class="col" v-if="option.en_option.length>0&&option.cn_option.length>0">&nbsp;</div>
		<div class="col-11" v-else>
			<pre v-text="option.x_option"></pre>
		</div>
	</div>
</div>

*/


const QuizOptionsComponent = Vue.extend({
    template: '' +
        '<div>\n' +
        '\t<div class="form-row" v-for="(option, index) in options" :for="prefix + `ABCDEFGHIJKL`[index]">\n' +
        '\t\t<div class="col">\n' +
        '\t\t\t<input :id="prefix + `ABCDEFGHIJKL`[index]" type="checkbox"\n' +
        '\t\t\t\t:name="prefix + `answer`" :value="`ABCDEFGHIJKL`[index]"\n' +
        '\t\t\t\tv-model="answer"\n' +
        '\t\t\t\tv-if="option.multi_choice">\n' +
        '\t\t\t<input :id="prefix + `ABCDEFGHIJKL`[index]" type="radio"\n' +
        '\t\t\t\t:name="prefix + `answer`" :value="`ABCDEFGHIJKL`[index]"\n' +
        '\t\t\t\tv-model="answer"\n' +
        '\t\t\t\tv-else>\n' +
        '\t\t\t<span v-text="`ABCDEFGHIJKL`[index] + `.`"></span>\n' +
        '\t\t</div>\n' +
        '\t\t<div class="col-5" v-if="option.en_option.length>0&&option.cn_option.length>0">\n' +
        '\t\t\t<pre v-text="option.en_option"></pre>\n' +
        '\t\t</div>\n' +
        '\t\t<div class="col-5" v-if="option.en_option.length>0&&option.cn_option.length>0">\n' +
        '\t\t\t<pre v-text="option.cn_option"></pre>\n' +
        '\t\t</div>\n' +
        '\t\t<div class="col" v-if="option.en_option.length>0&&option.cn_option.length>0">&nbsp;</div>\n' +
        '\t\t<div class="col-11" v-else>\n' +
        '\t\t\t<pre v-text="option.x_option"></pre>\n' +
        '\t\t</div>\n' +
        '\t</div>\n' +
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
            default: '',
        },
        index: {
            type: Number,
            require: false,
            default: -1,
        },
    },
    computed: {
        answer: {
            get() {
                if (this.index >= 0) {
                    return this.question.a[this.index];
                } else {
                    return this.question.a;
                }
            },
            set(val) {
                if (this.index >= 0) {
                    this.question.a[this.index] = val;
                } else {
                    this.question.a = val;
                }
            },
        },
    },
});

Vue.component('quiz-options-component', QuizOptionsComponent);