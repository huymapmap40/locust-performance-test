
"""
- Used the following query to pull users with decent number of orders (0-30). But make sure
the account does not have a lot of linked accounts. Generally, QA accounts have a lot of linked
accounts and are hence not usable. Check with risk team to see the linked accounts for a user.

select account_id, count(id) as total_orders from pay_later_order
where status = 'accepted'
group by account_id
order by total_orders desc
"""
users_with_some_orders = [101828974,101828855]

"""
- Use separate users for fetching user summary and order creation, as otherwise get summary api might be too slow
and might not produce realistic results.
- Make sure users are KYC approved and have payment methods.
- To check KYC status use: https://needle-dev.shopback.com/customer/profile/:accountId/overview
- To check payment methods: https://needle-dev.shopback.com/alfred/v2?accountId={accountId}
"""
users_for_static_orders = [101829040, 101829041]


