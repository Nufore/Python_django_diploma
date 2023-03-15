var mix = {
    // может это сделать через шаблонизатор?
    computed: {
      tags () {
          return this.topTags.filter(tag => this.product?.tags?.includes(tag.id))
      }
    },
    methods: {
        changeCount (value) {
            this.count = this.count + value
            if (this.count < 1) this.count = 1
            console.log('count', this.count)
        },
        getProduct() {
            const productId = location.pathname.startsWith('/product/')
            ? Number(location.pathname.replace('/product/', ''))
            : null
            this.getData(`/api/products/${productId}`).then(data => {
                this.product = {
                    ...this.product,
                    ...data
                }
            }).catch(() => {
                const product = this.catalogFromServer.find(el => el.id === productId) ?? {}
                this.product = {
                    ...this.product,
                    ...product,
                    fullDescription: 'description description description description description description description description description description description description description description description description description description ',
                    specifications: [
                        { name: 'Size', value: 'XL' },
                        { name: 'Size', value: 'XL' },
                        { name: 'Size', value: 'XL' },
                        { name: 'Size', value: 'XL' },
                        { name: 'Width', value: '500' },
                        { name: 'Width', value: '500' },
                        { name: 'Width', value: '500' },
                        { name: 'Width', value: '500' },
                        { name: 'Width', value: '500' },
                    ],
                    reviews: [
                        { author: 'Orange', date: '2022-01-30 12:58', text: 'nice!', rate: 5 },
                        { author: 'Apple', date: '2022-01-25 12:18', text: 'bad!!!', rate: 2 },
                    ]
                }
                console.log('product', product)
            })
        },
        submitReview () {
            this.postData('/api/review', {
                author: this.review.author,
                email: this.review.email,
                text: this.review.text,
                rate: this.review.rate
            }).then(data => {
                this.product.reviews = data
            }).catch(() => {
                this.product.reviews.push({
                    ...this.review,
                    date: '2023-05-05 12:12'
                })
            }).finally(() => {
                this.review.author = ''
                this.review.email = ''
                this.review.text = ''
                this.review.rate = 5
            })
        }
    },
    mounted () {
        this.getProduct();
    },
    data() {
        return {
            product : {},
            count: 1,
            review: {
                author: '',
                email: '',
                text: '',
                rate: 5
            }
        }
    },
}