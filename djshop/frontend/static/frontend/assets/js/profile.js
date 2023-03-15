var mix = {
    methods: {
        getProfile(userId) {
            this.getData(`/api/profile/`).then(data => {
                this.fullName = data.fullName
                this.avatar = data.avatar
                this.phone = data.phone
                this.email = data.email
            }).catch(() => {
                this.fullName = 'Полное имя'
                this.avatar = 'https://i.pravatar.cc/300'
                this.phone = '88002000600'
                this.email = 'no-reply@mail.ru'
            })
        },
        changeProfile () {
            if(!this.fullName.trim().length || !this.phone.trim().length || !this.email.trim().length) {
                alert('В форме присутствуют незаполненные поля')
                return
            }

            this.postData('/api/profile/change', {
                fullName: this.fullName,
                avatar: this.avatar,
                phone: this.phone,
                email: this.email
            }).then(data => {
               alert('Успешно сохранено')
            }).catch(() => {
               alert('Ошибка сохранения')
            }).finally(() => {})
        },
        changePassword () {
            if (
                !this.passwordCurrent.trim().length ||
                !this.password.trim().length ||
                !this.passwordReply.trim().length ||
                this.password !== this.passwordReply
            ) {
                alert('В форме присутствуют незаполненные поля или пароли не совпадают')
                return
            }
            this.postData('/api/profile/password').then(data => {
               alert('Успешно сохранено')
            }).catch(() => {
                alert('Ошибка сохранения')
            }).finally(() => {
                this.passwordCurrent = ''
                this.password = ''
                this.passwordReply = ''
            })
        }
    },
    created() {
        this.getProfile();
    },
    data() {
        return {
            fullName: null,
            phone: null,
            email: null,
            avatar: null,
            password: '',
            passwordCurrent: '',
            passwordReply: ''
        }
    },
}