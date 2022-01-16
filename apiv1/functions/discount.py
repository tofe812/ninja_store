dis_list = [
    {
        'discount_name': 'dsp30',
        'discount_type': 'percentage',
        'max_discount': '3000',
        'discount_value': '30',
        'active': True,
    },
    {
        'discount_name': 'dsf3000',
        'discount_type': 'fixed',
        'max_discount': '3000',
        'discount_value': '3000',
        'active': True,
    },
]


def main():
    total_price = 3000
    get_discount_id = 1
    # total_price = input('Enter total price: ')
    # get_discount_id = int(input('Enter discount id: '))

    discount = dis_list[get_discount_id]
    discount_price = 0

    if discount['active']:
        print('Discount is active')
        print(discount['discount_type'])
        if discount['discount_type'] == 'percentage':
            discount_value = float(total_price) * float(discount['discount_value']) / 100
            if discount_value > float(discount['max_discount']):
                discount_value = float(discount['max_discount'])
            print(discount_value)
            discount_price = float(total_price) - discount_value
        elif discount['discount_type'] == 'fixed':
            if float(discount['discount_value']) >= total_price:
                print('its free!!')
            else:
                discount_price = float(total_price) - float(discount['discount_value'])

        else:
            print('Invalid discount type')
    else:
        print('Discount is not active')
    print(discount_price)


main()
