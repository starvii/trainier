/*

<div>
	<label class="form-row" v-for="(option, index) in trunk.options">
		<div class="col">
			<input type="checkbox"
				:name="trunk.entity_id" :value="option.entity_id"
				v-model="answer"
				v-if="trunk.multi_choice">
			<input type="radio"
				:name="trunk.entity_id" :value="option.entity_id"
				v-model="answer"
				v-else>
			<span v-text="`ABCDEFGHIJKL`[index] + `.`"></span>
		</div>
		<div class="col-6" v-if="option.en_option.length>0&&option.cn_option.length>0">
			<pre v-text="option.en_option"></pre>
		</div>
		<div class="col-5" v-if="option.en_option.length>0&&option.cn_option.length>0">
			<pre v-text="option.cn_option"></pre>
		</div>
		<div class="col-11" v-else>
			<pre v-text="option.x_option"></pre>
		</div>
	</label>
</div>

*/


const QuizOptionsComponent = Vue.extend({
    template: '' +
        '<div>\n' +
        '\t<label class="form-row" v-for="(option, index) in trunk.options">\n' +
        '\t\t<div class="col">\n' +
        '\t\t\t<input type="checkbox"\n' +
        '\t\t\t\t:name="trunk.entity_id" :value="option.entity_id"\n' +
        '\t\t\t\tv-model="answer_wrapper.answer[trunk.entity_id]"\n' +
        '\t\t\t\tv-if="trunk.multi_choice">\n' +
        '\t\t\t<input type="radio"\n' +
        '\t\t\t\t:name="trunk.entity_id" :value="option.entity_id"\n' +
        '\t\t\t\tv-model="answer_wrapper.answer[trunk.entity_id]"\n' +
        '\t\t\t\tv-else>\n' +
        '\t\t\t<span v-text="`ABCDEFGHIJKL`[index] + `.`"></span>\n' +
        '\t\t</div>\n' +
        '\t\t<div class="col-6" v-if="option.en_option.length>0&&option.cn_option.length>0">\n' +
        '\t\t\t<pre v-text="option.en_option"></pre>\n' +
        '\t\t</div>\n' +
        '\t\t<div class="col-5" v-if="option.en_option.length>0&&option.cn_option.length>0">\n' +
        '\t\t\t<pre v-text="option.cn_option"></pre>\n' +
        '\t\t</div>\n' +
        '\t\t<div class="col-11" v-else>\n' +
        '\t\t\t<pre v-text="option.x_option"></pre>\n' +
        '\t\t</div>\n' +
        '\t</label>\n' +
        '</div>',
    replace: true,
    // data() {
    //     return {
    //         privateAnswer: [],
    //     };
    // },
    // computed: {
    //     protectedAnswer: {
    //         get() {
    //             return this.privateAnswer;
    //         },
    //         set(val) {
    //             this.privateAnswer = val;
    //             this.$emit('change', {
    //                 trunk: this.trunk.entity_id,
    //                 answer: val,
    //             });
    //         },
    //     }
    // },
    // watch: {
    //     answer(newVal, oldVal) {
    //         console.debug(`old = ${oldVal}, new = ${newVal}`);
    //         this.protectedAnswer = newVal;
    //     },
    // },
    props: {
        trunk: {
            type: Object,
            require: true,
        },
        answer_wrapper: { // 为了解决修改是告警问题
            type: Object,
            require: true,
        },
    },
});

Vue.component('quiz-options-component', QuizOptionsComponent);