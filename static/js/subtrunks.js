// sub (children) trunks

/*

<div>
	<div id="trunk-children" v-for="(trunk, index) in trunks">
		<hr/>
		<div class="row">
			<strong class="col" v-text="`第` + (index + 1) + `题`"></strong>
			<div class="col justify-content-end">
				<button type="button" class="btn btn-sm btn-outline-danger float-right"
					style="margin-left: 3px; margin-right: 3px;"
					@click="removeTrunk(index)">
					<i class="fas fa-minus"></i>
				</button>
				<button type="button" class="btn btn-sm btn-outline-success float-right"
					style="margin-left: 3px; margin-right: 3px;"
					@click="insertTrunk(index)">
					<i class="fas fa-plus"></i>
				</button>
			</div>
		</div>
		<trunk-component :trunk.sync="trunk"></trunk-component>
	</div>
</div>

*/


const TrunksComponent = Vue.extend({
    template: '' +
        '<div>\n' +
        '\t<div id="trunk-children" v-for="(trunk, index) in trunks">\n' +
        '\t\t<hr/>\n' +
        '\t\t<div class="row">\n' +
        '\t\t\t<strong class="col" v-text="`第` + (index + 1) + `题`"></strong>\n' +
        '\t\t\t<div class="col justify-content-end">\n' +
        '\t\t\t\t<button type="button" class="btn btn-sm btn-outline-danger float-right"\n' +
        '\t\t\t\t\tstyle="margin-left: 3px; margin-right: 3px;"\n' +
        '\t\t\t\t\t@click="removeTrunk(index)">\n' +
        '\t\t\t\t\t<i class="fas fa-minus"></i>\n' +
        '\t\t\t\t</button>\n' +
        '\t\t\t\t<button type="button" class="btn btn-sm btn-outline-success float-right"\n' +
        '\t\t\t\t\tstyle="margin-left: 3px; margin-right: 3px;"\n' +
        '\t\t\t\t\t@click="insertTrunk(index)">\n' +
        '\t\t\t\t\t<i class="fas fa-plus"></i>\n' +
        '\t\t\t\t</button>\n' +
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