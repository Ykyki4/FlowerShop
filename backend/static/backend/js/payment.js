document.querySelector("#submit_button").addEventListener("click", () => {
    fetch("/yookassa-config/")
    .then((result) => { return result.json(); })
    .then((data) => {
        const checkout = YooMoneyCheckout(data.shop_id, {
        language: 'ru'
        });
        checkout.tokenize({
            number: document.querySelector('.number').value,
            cvc: document.querySelector('.cvc').value,
            month: document.querySelector('.expiry_month').value,
            year: document.querySelector('.expiry_year').value
        }).then(res => {
            if (res.status === 'success') {
                const { paymentToken } = res.data.response;
                document.querySelector('.payment_token').value = paymentToken;
                console.log(document.querySelector('.payment_token').value);
                document.querySelector('.orderStep_form').submit();
            }
        });
    });
});