{{ config(materialized='table') }}

with orders as (
    select * from {{ ref('stg_orders') }}
),

order_items as (
    select 
        order_id,
        product_id,
        sum(price) as total_price,
        sum(freight_value) as total_freight
    from {{ source('public', 'order_items') }}
    group by 1, 2
),

customers as (
    select * from {{ ref('stg_customers') }}
),

products as (
    select * from {{ ref('stg_products') }}
)

select
    -- Order Info
    o.order_id,
    o.order_status,
    
    -- Customer Info
    c.customer_unique_id,
    c.city as customer_city,
    c.state as customer_state,
    
    -- Product Info
    p.product_id,
    p.category_name,
    
    -- Metrics
    oi.total_price,
    oi.total_freight,
    o.purchase_at,
    o.delivered_customer_at,
    extract(day from (o.delivered_customer_at - o.purchase_at)) as days_to_deliver,
    extract(day from (o.estimated_delivery_at - o.delivered_customer_at)) as arrival_vs_estimated
    
from orders o
left join order_items oi on o.order_id = oi.order_id
left join customers c on o.customer_id = c.customer_id
left join products p on oi.product_id = p.product_id
where o.order_status = 'delivered'