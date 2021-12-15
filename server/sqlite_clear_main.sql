BEGIN;
DELETE FROM "main_smslog";
DELETE FROM "main_tag";
DELETE FROM "main_picture";
DELETE FROM "main_subscription_user";
DELETE FROM "main_category";
DELETE FROM "main_seller";
DELETE FROM "main_subscription";
DELETE FROM "main_ad";
DELETE FROM "main_ad_tags";
UPDATE "sqlite_sequence"
SET "seq" = 0
WHERE "name" IN ('main_smslog', 'main_tag', 'main_picture', 'main_subscription_user', 'main_category', 'main_seller',
                 'main_subscription', 'main_ad', 'main_ad_tags');
COMMIT;
