var mix = {
    methods: {
        getCartItems() {
            this.getData("/api/cart")
              .then(data => {
                this.cartProducts = data.items
              })
        },
        submitBasket () {
            this.postData('/api/order', Object.values(this.basket))
                .then(data => {
                    this.order.id = data.id
                    this.order.products = data.products
                    this.basket = {}
                }).catch(() => {
                    this.order.id = Date.now()
                    this.order.products = Object.values(this.basket)
                    // this.basket = {}
                    // window.localStorage.setItem('basket', JSON.stringify(this.basket))
                    window.localStorage.setItem('order', JSON.stringify(this.order))
                }).finally(() => {
                    location.assign('/order')
                })
        }
    },
    mounted() {
        // this.getCartItems();
    },
    data() {
        return {
            cartProducts: [],
        }
    }
}