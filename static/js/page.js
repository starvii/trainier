/*

<nav name="page-list">
	<div name="pagination" v-if="conf.totalItems>0">
		<ul class="pagination pagination-sm m-0 float-right">
			<li class="page-item" :class="{disabled:conf.currentPage==1}">
				<a class="page-link" :class="{disabled:conf.currentPage==1}" @click="prevPage()">
					<i class="fas fa-angle-left"></i>
				</a>
			</li>
			<li class="page-item"
				:class="{active:item==conf.currentPage,disabled:item=='...'}"
				v-for="(item, index) in pageList">
				<a class="page-link" v-if="item=='...'" v-text="item"
					style="{cursor: default; border-top:none; border-bottom:none;} :hover {background: none}">
				</a>
				<a class="page-link" v-else
					@click="changeCurrentPage(item)" v-text="item">
				</a>
			</li>
			<li class="page-item" :class="{disabled:conf.currentPage==conf.numberOfPages}">
				<a class="page-link"
					:class="{disabled:conf.currentPage==conf.numberOfPages}"
					@click="nextPage()">
					<i class="fas fa-angle-right"></i>
				</a>
			</li>
		</ul>
		<form name=pate-total class="form-inline m-0">
			<div class="form-group px-sm-3">
				<label>第</label>
				<input class="form-control form-control-sm mx-sm-2"
					type="text"
					v-model="jumpPageNum"
					@keyup.enter="jumpToPage($event)"
				/>
				<label>页</label>
			</div>
			<div class="form-group px-sm-3">
				<label>每页</label>
				<select class="form-control form-control-sm mx-sm-2"
					v-model="conf.itemsPerPage"
				>
					<option v-for="option in conf.perPageOptions" v-text="option"></option>
				</select>
				<label>/共<strong v-text="conf.totalItems"></strong>条</label>
			</div>
		</form>
	</div>
	<div name="no-items" v-else>
		<strong>无数据</strong>
	</div>
</nav>

*/


const PageComponent = Vue
    .extend({
        template: '' +
            '<nav name="page-list">\n' +
            '\t<div name="pagination" v-if="conf.totalItems>0">\n' +
            '\t\t<ul class="pagination pagination-sm m-0 float-right">\n' +
            '\t\t\t<li class="page-item" :class="{disabled:conf.currentPage==1}">\n' +
            '\t\t\t\t<a class="page-link" :class="{disabled:conf.currentPage==1}" @click="prevPage()">\n' +
            '\t\t\t\t\t<i class="fas fa-angle-left"></i>\n' +
            '\t\t\t\t</a>\n' +
            '\t\t\t</li>\n' +
            '\t\t\t<li class="page-item"\n' +
            '\t\t\t\t:class="{active:item==conf.currentPage,disabled:item==\'...\'}"\n' +
            '\t\t\t\tv-for="(item, index) in pageList">\n' +
            '\t\t\t\t<a class="page-link" v-if="item==\'...\'" v-text="item"\n' +
            '\t\t\t\t\tstyle="{cursor: default; border-top:none; border-bottom:none;} :hover {background: none}">\n' +
            '\t\t\t\t</a>\n' +
            '\t\t\t\t<a class="page-link" v-else\n' +
            '\t\t\t\t\t@click="changeCurrentPage(item)" v-text="item">\n' +
            '\t\t\t\t</a>\n' +
            '\t\t\t</li>\n' +
            '\t\t\t<li class="page-item" :class="{disabled:conf.currentPage==conf.numberOfPages}">\n' +
            '\t\t\t\t<a class="page-link"\n' +
            '\t\t\t\t\t:class="{disabled:conf.currentPage==conf.numberOfPages}"\n' +
            '\t\t\t\t\t@click="nextPage()">\n' +
            '\t\t\t\t\t<i class="fas fa-angle-right"></i>\n' +
            '\t\t\t\t</a>\n' +
            '\t\t\t</li>\n' +
            '\t\t</ul>\n' +
            '\t\t<form name=pate-total class="form-inline m-0">\n' +
            '\t\t\t<div class="form-group px-sm-3">\n' +
            '\t\t\t\t<label>第</label>\n' +
            '\t\t\t\t<input class="form-control form-control-sm mx-sm-2"\n' +
            '\t\t\t\t\ttype="text"\n' +
            '\t\t\t\t\tv-model="jumpPageNum"\n' +
            '\t\t\t\t\t@keyup.enter="jumpToPage($event)"\n' +
            '\t\t\t\t/>\n' +
            '\t\t\t\t<label>页</label>\n' +
            '\t\t\t</div>\n' +
            '\t\t\t<div class="form-group px-sm-3">\n' +
            '\t\t\t\t<label>每页</label>\n' +
            '\t\t\t\t<select class="form-control form-control-sm mx-sm-2"\n' +
            '\t\t\t\t\tv-model="conf.itemsPerPage"\n' +
            '\t\t\t\t>\n' +
            '\t\t\t\t\t<option v-for="option in conf.perPageOptions" v-text="option"></option>\n' +
            '\t\t\t\t</select>\n' +
            '\t\t\t\t<label>/共<strong v-text="conf.totalItems"></strong>条</label>\n' +
            '\t\t\t</div>\n' +
            '\t\t</form>\n' +
            '\t</div>\n' +
            '\t<div name="no-items" v-else>\n' +
            '\t\t<strong>无数据</strong>\n' +
            '\t</div>\n' +
            '</nav>',
        replace: true,
        props: {
            conf: {
                type: Object,
                require: true,
            },
        },
        data() {
            return {
                jumpPageNum: '',
                pageList: [],
            };
        },
        computed: {
            totalItems() {
                return `/共${this.conf.totalItems}条`;
            }
        },
        mounted() {
            this.conf.pagesLength = parseInt(this.conf.pagesLength) ? parseInt(this.conf.pagesLength)
                : 9;
            if (this.conf.pagesLength % 2 === 0) {
                // 如果不是奇数的时候处理一下
                this.conf.pagesLength = this.conf.pagesLength - 1;
            }

            // conf.perPageOptions
            if (this.conf.perPageOptions) {
                this.conf.perPageOptions = [10, 15, 30, 50, 100];
            }

            this.$watch(this.getWatchState, this.getPagination);
            this.getPagination();
        },
        methods: {
            changeCurrentPage(item) {
                if (item === '...') {
                    // return;
                } else {
                    this.conf.currentPage = item;
                }
            },

            // pageList数组
            getPagination(newValue, oldValue) {

                // conf.currentPage
                this.conf.currentPage = parseInt(this.conf.currentPage) ? parseInt(this.conf.currentPage)
                    : 1;

                // conf.totalItems
                this.conf.totalItems = parseInt(this.conf.totalItems) ? parseInt(this.conf.totalItems)
                    : 0;

                // conf.itemsPerPage (default:15)
                this.conf.itemsPerPage = parseInt(this.conf.itemsPerPage) ? parseInt(this.conf.itemsPerPage)
                    : 10;

                // numberOfPages
                this.conf.numberOfPages = Math.ceil(this.conf.totalItems
                    / this.conf.itemsPerPage);

                // judge currentPage > numberOfPages
                if (this.conf.currentPage < 1) {
                    this.conf.currentPage = 1;
                }

                // 如果分页总数>0，并且当前页大于分页总数
                if (this.conf.numberOfPages > 0
                    && this.conf.currentPage > this.conf.numberOfPages) {
                    this.conf.currentPage = this.conf.numberOfPages;
                }

                // jumpPageNum
                this.jumpPageNum = this.conf.currentPage;

                // 如果itemsPerPage在不在perPageOptions数组中，就把itemsPerPage加入这个数组中
                let perPageOptionsLength = this.conf.perPageOptions.length;
                // 定义状态
                let perPageOptionsStatus;
                for (var i = 0; i < perPageOptionsLength; i++) {
                    if (this.conf.perPageOptions[i] === this.conf.itemsPerPage) {
                        perPageOptionsStatus = true;
                    }
                }
                // 如果itemsPerPage在不在perPageOptions数组中，就把itemsPerPage加入这个数组中
                if (!perPageOptionsStatus) {
                    this.conf.perPageOptions.push(this.conf.itemsPerPage);
                }

                // 对选项进行sort
                this.conf.perPageOptions.sort(function (a, b) {
                    return a - b
                });

                this.pageList = [];
                if (this.conf.numberOfPages <= this.conf.pagesLength) {
                    // 判断总页数如果小于等于分页的长度，若小于则直接显示
                    for (i = 1; i <= this.conf.numberOfPages; i++) {
                        this.pageList.push(i.toString());
                    }
                } else {
                    // 总页数大于分页长度（此时分为三种情况：1.左边没有···2.右边没有···3.左右都有···）
                    // 计算中心偏移量
                    let offset = (this.conf.pagesLength - 1) / 2;
                    if (this.conf.currentPage <= offset) {
                        // 左边没有···
                        for (i = 1; i <= offset + 1; i++) {
                            this.pageList.push(i);
                        }
                        this.pageList.push('...');
                        this.pageList.push(this.conf.numberOfPages);
                    } else if (this.conf.currentPage > this.conf.numberOfPages - offset) {
                        this.pageList.push(1);
                        this.pageList.push('...');
                        for (i = offset + 1; i >= 1; i--) {
                            this.pageList.push(this.conf.numberOfPages - i);
                        }
                        this.pageList.push(this.conf.numberOfPages);
                    } else {
                        // 最后一种情况，两边都有...
                        this.pageList.push(1);
                        this.pageList.push('...');

                        for (i = Math.ceil(offset / 2); i >= 1; i--) {
                            this.pageList.push(this.conf.currentPage - i);
                        }
                        this.pageList.push(this.conf.currentPage);
                        for (i = 1; i <= offset / 2; i++) {
                            this.pageList.push(this.conf.currentPage + i);
                        }

                        this.pageList.push('...');
                        this.pageList.push(this.conf.numberOfPages);
                    }
                }

                // 防止初始化两次请求问题
                let functionOnChange;
                if (this.conf.onChange) {
                    if (this.$parent.$options.methods[this.conf.onChange]) {
                        functionOnChange = this.$parent.$options.methods[this.conf.onChange];
                    }
                }
                if (functionOnChange) {
                    if (!(oldValue !== newValue && oldValue[0] === 0)) {
                        // 根据时间判断，500ms内不做第二次请求
                        // if (!this.conf.timestamp) { this.conf.timestamp = 0; }
                        // let now = new Date().getTime();
                        // if (now - this.conf.timestamp <= 500)
                        // {
                        //     //console.debug('timestamp <= 500');
                        //     return;
                        // }
                        // this.conf.timestamp = now;


                        // 执行查询
                        console.debug(`newVal = ${newValue}, oldVal = ${oldValue}`);
                        console.debug(this.getWatchState());
                        functionOnChange.apply(this.$parent);
                    }
                }
            },

            prevPage() {
                if (this.conf.currentPage > 1) {
                    this.conf.currentPage -= 1;
                }
            },

            nextPage() {
                if (this.conf.currentPage < this.conf.numberOfPages) {
                    this.conf.currentPage += 1;
                }
            },

            jumpToPage() {
                let pn = this.jumpPageNum.toString().replace(/[^0-9]/g, '');
                if (pn !== '') {
                    this.jumpPageNum = parseInt(pn);
                    this.conf.currentPage = parseInt(pn);
                }
            },

            getWatchState() {
                if (!this.conf.totalItems) {
                    this.conf.totalItems = 0;
                }
                return this.conf.totalItems + ' ' + this.conf.currentPage + ' ' + this.conf.itemsPerPage;
            },
        },
    });

Vue.component('page-component', PageComponent);
