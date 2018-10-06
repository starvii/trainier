// sub (children) trunks

/*

<div class="container">
	<div class="container" id="trunk-children" v-for="(trunk, index) in trunks">
		<hr/>
		<div class="level">
			<div class="level-left">
				<div class="level-item">
					<div class="subtitle" v-text="`第` + index + `题`"></div>
				</div>
			</div>
			<div class="level-right">
				<div class="level-item">
					<a class="button is-link is-success" @click="insertTrunk(index)">添加</a>
				</div>
				<div class="level-item">
					<a class="button is-link is-success" @click="removeTrunk(index)">删除</a>
				</div>
			</div>
		</div>
		<trunk-component :trunk.sync="trunk"></trunk-component>
	</div>
</div>

*/


const TrunksComponent = Vue.extend({
    template: '' +
        '<div class="container">\n' +
        '\t<div class="container" id="trunk-children" v-for="(trunk, index) in trunks">\n' +
        '\t\t<hr/>\n' +
        '\t\t<div class="level">\n' +
        '\t\t\t<div class="level-left">\n' +
        '\t\t\t\t<div class="level-item">\n' +
        '\t\t\t\t\t<div class="subtitle" v-text="`第` + (index + 1) + `题`"></div>\n' +
        '\t\t\t\t</div>\n' +
        '\t\t\t</div>\n' +
        '\t\t\t<div class="level-right">\n' +
        '\t\t\t\t<div class="level-item">\n' +
        '\t\t\t\t\t<a class="button is-link is-success" @click="insertTrunk(index)">添加</a>\n' +
        '\t\t\t\t</div>\n' +
        '\t\t\t\t<div class="level-item">\n' +
        '\t\t\t\t\t<a class="button is-link is-success" @click="removeTrunk(index)">删除</a>\n' +
        '\t\t\t\t</div>\n' +
        '\t\t\t</div>\n' +
        '\t\t</div>\n' +
        '\t\t<trunk-component :trunk.sync="trunk"></trunk-component>\n' +
        '\t</div>\n' +
        '</div>',
    replace: true,
    props: {
        trunks: {
            type: Array,
            require: true,
        },
    },
    mounted: function () {
    },
    methods: {
        insertTrunk: function (index) {
            let idx = index + 1;
            this.trunks.splice(idx, 0, {});
            this.$set(this.trunks, idx, newTrunk());
        },
        removeTrunk: function (index) {
            if (this.trunks.length > 1) {
                this.trunks.splice(index, 1);
            }
        },
    },
});

Vue.component('trunks-component', TrunksComponent);