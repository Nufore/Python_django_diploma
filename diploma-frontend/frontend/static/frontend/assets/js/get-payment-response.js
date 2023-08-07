var mix = {
    methods: {
        getPaymentResponse() {
            const paymentId = location.pathname.startsWith('/progress-payment/')
            ? Number(location.pathname.replace('/progress-payment/', '').replace('/', ''))
            : null
            this.getData(`/api/get-payment-response/${paymentId}`).then(data => {
                this.data = {
                    ...this.data,
                    ...data
                }
                if(!data.data) {
                    console.log(data.data)
                    setTimeout(this.getPaymentResponse(), 50000)
                } else {
                    location.replace(`/order-detail/${paymentId}/`)
                }
            }).catch(() => {
                this.product = {}
                console.warn('Ошибка при получении товара')
            })
        },
    },
    mounted () {
        setTimeout(this.getPaymentResponse(), 10000);
    },
    data() {
        return {
            data : false
        }
    },
}