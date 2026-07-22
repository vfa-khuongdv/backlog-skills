## Description

Add user coin analytics dashboard with real-time balance tracking and monthly bonus distribution. This PR introduces the `getCoinReportSummary` API, enhances bonus distribution with atomic transaction logging, and adds pagination to coin history.

Ticket: #20344 (extracted from branch `feature/20344-coin-analytics`)

---

## Key Features

- `getCoinReportSummary` query — total coins, bonus coins, earned coins, and expiration data
- `addMonthlyBonusCoin` mutation — bulk bonus distribution with atomic rollback via Prisma `$transaction`
- `users_transactions` table — full audit trail per coin operation with type and source tracking
- Paginated `getCoinHistory` with date-range filtering and sort order

---

## Changes Made

- **Added `getCoinReportSummary` resolver** in `coin.resolver.ts` — aggregates totalHP, bonusCoins, earnedCoins, expiresAt from user and transaction records
- **Added `addMonthlyBonusCoin` mutation** in `coin.service.ts` — bulk insert and update wrapped in Prisma `$transaction` with per-user audit record
- **Added `CoinReportDto`** in `dto/coin-report.dto.ts` — validation via `@IsNumber` and `@IsDate` decorators
- **Added `users_transactions` table** via migration `20240715_add_coin_transactions` — columns: userId, amount, type (enum), source, createdAt
- **Updated `prisma/schema.prisma`** — new `UsersTransaction` model with `@@index([userId, type])` for query performance
- **Updated `CoinService.getHistory`** — added `PaginationDto` supporting limit, offset, fromDate, toDate
- **Added `coin.config.ts`** — `MONTHLY_BONUS_AMOUNT` and `BONUS_EXPIRY_DAYS` constants
- **Tests** — 12 unit tests (single, bulk, empty, duplicate, rollback, zero-amount edge cases) + 4 e2e tests (full bonus flow, report summary, pagination boundary, unauthorized access)

---

## Self-Review

- [x] Functionality — tested bonus mutation with single user, 100 users, empty array, and mid-batch rollback; verified report breakdown for 0 bonus, partial bonus, fully expired bonus; confirmed pagination handles limit=0, offset beyond total, and negative values
- [x] Security — all inputs validated via `class-validator` DTOs; mutations gated behind `@UseGuards(AuthGuard)`; userId extracted from JWT context, not request params; Prisma parameterized queries prevent injection
- [x] Error Handling — all bonus writes wrapped in `$transaction` with full rollback on any failure; typed `HttpException` with descriptive messages (`NOT_FOUND`, `BAD_REQUEST`); logger records warnings on rollback events
- [x] Code Quality — ESLint and Prettier pass with zero errors; JSDoc on all public methods with `@param`, `@returns`, `@throws`; no magic numbers — all constants in `coin.config.ts`
- [x] Dependencies — zero new packages added; only uses existing NestJS core, Prisma, and class-validator

---

## Manual Test Steps

1. **Test bonus distribution:**
   - Call `addMonthlyBonusCoin` mutation with `userIds: ["uuid-a", "uuid-b", "uuid-c"]`
   - Verify all 3 users have `totalHP` and `totalHGPCBonusCoin` incremented by `MONTHLY_BONUS_AMOUNT`
   - Check `users_transactions` table has 3 new rows with `type = 'MONTHLY_BONUS'` and correct `amount`

2. **Test rollback on failure:**
   - Call `addMonthlyBonusCoin` with an invalid UUID in the middle: `["uuid-a", "bad-id", "uuid-c"]`
   - Verify mutation returns error, user "uuid-a" coin values unchanged
   - Confirm zero rows added to `users_transactions` — full rollback

3. **Test coin report summary:**
   - Seed user with 500 earned coins + 200 bonus coins (100 active, 100 expired)
   - Call `getCoinReportSummary` — verify `totalCoins: 700`, `bonusCoins: 200`, `activeBonus: 100`, `expiredBonus: 100`
   - Confirm `expiresAt` is 30 days from bonus creation date

4. **Test pagination:**
   - Seed 25 transaction records for a user
   - Call `getCoinHistory(limit: 10, offset: 0)` → expect 10 results, newest first
   - Call `getCoinHistory(limit: 10, offset: 20)` → expect 5 results
   - Call `getCoinHistory(limit: 10, offset: 30)` → expect empty array
