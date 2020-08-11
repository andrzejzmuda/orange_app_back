delete from assets_asset lg where not exists (
    select from assets_history lr where lr.asset_id = lg.id
);