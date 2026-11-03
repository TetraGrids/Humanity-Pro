# Protocol todos

Source of truth for finishing the Humanity Pro protocol. Managed by `.cursor/skills/protocol-todos/SKILL.md`.

This file is not `TO-DO-B4-MAINNET.md`. Rows here stay after they are done, with history. IDs are never reused.

Each todo has a **Completeness** list. Those checks are how the finished work is verified. A todo is done only when every check passes.

Audit date: 2026-10-27. HP-01 has renamed the product and operational surface to **Humanity Pro**, but its local binary build is blocked by host/submodule toolchain incompatibilities. Contracts that already run are listed under [Already in the tree](#already-in-the-tree).

## List

- [ ] HP-01 — Convert all from the previous repo to rename to Humanity Pro — in progress
- [ ] HP-02 — Fix `ra.bpay` reward distribution so an inactive producer cannot hang the transfer — in progress
- [ ] HP-03 — Pay producers and owed work from activity fees, not from new RA inflation — open
- [ ] HP-04 — Make a Pure Liquid token actually locked ranged liquidity for its whole supply — open
- [ ] HP-05 — Let a holder opt out of the activity tax — open
- [ ] HP-06 — Replace trusted relayer credit with on-chain deposit proofs — open
- [ ] HP-07 — Add non-aborting key recovery and a contract-readable permission read — open
- [ ] HP-08 — Social recovery: unusual or large transfers need upstream confirmation — open
- [ ] HP-09 — Time-based daily RA for attention, not a new inflation print — open
- [ ] HP-10 — Weight proposals by a verified person, then activity, then a living graph — open
- [ ] HP-11 — Offers: an action, a RA cost or payment, and a check that it was done — open
- [ ] HP-12 — Passport: one record per human, stamps, accolades, connections that fade — open
- [ ] HP-13 — Discovery: regional, then national, then global attention charts — open
- [ ] HP-14 — Recurve: small-room elections that put an oath on the record — open
- [ ] HP-15 — Localize: a region turns on when people stake and found it — open
- [ ] HP-16 — Carnivals: a three-month season whose accolades land on the Passport — open
- [ ] HP-17 — Chain tests for `ra.org`, `ra.resources`, and `flex.token` — open

## Already in the tree

Do not re-file these. They are the base the todos above sit on.

- Node: Spring 2.0 / Savanna. Binaries `humanityd`, `humanity`, `humanity-keyd`, `humanity-util`. System token **RA** (4 decimals). System account `ra`.
- `ra.system`: fixed-price RAM (0.0020 RA/byte, 10% fee), age caps, `buyramsys` / `sellramsys`, `ramlimitset`, app registry and `loginwithapp`, powerup. REX actions abort in `assert_rex_disabled()` (`contracts/ra.system/src/rex.cpp`). Stake-weighted producer voting and inflationary `claimrewards` are still the Spring path (`contracts/ra.system/src/voting.cpp`, `producer_pay.cpp`).
- `ra.resources`: CPU/NET plans paid from a pool funded by a RA transfer with memo `fund`. Deployed by `scripts/launch-devnet.py`.
- `ra.authex` / `ra.claim`: self-attested links, `linksig` / `claimsig` / `creditopen` / `claimopen` for EM and ED keys. Relayer `credit` is still the deposit record. Tests: `unittests/ra.claim_tests.cpp`. Design notes: `contracts/ra.claim/FUTURE.md`.
- `ra.org`: roles, seats, self/manager/peer review, monthly close, trickle of an incoming buck token. No chain test.
- `flex.token` (`contracts/ra.pure/`): forge, mint, transfer tax into reflection / burn / project pools, `reflect`, `interestoken`, `inheritance`, `openpool` / `seedpool` / `collectpool` as inline calls to an external Alcor-style swap (default `swap.alcor`). ABI surface check only: `tests/interface/test_deploy_surface.py`.
- `ra.fees`: accepts RA and, if a REX pool has `total_rex > 0`, tries `donatetorex`. Otherwise the tokens sit. No split to producers or `ra.org`.

## HP-01 — Convert all from the previous repo to rename to Humanity Pro

**Status:** in progress

### Context

At filing time, only the checkout folder and GitHub remote used Humanity Pro. The protocol text, binaries, CMake, genesis, contract comments, tests, scripts, and docs paths still used the former product and operational names.

The renamed surface now uses:

- Product title and body: Humanity Pro in `README.md`, `CONTRIBUTING.md`, `WHITEPAPER.md`, `PURE-LIQUID.md`, `genesis/README.md`, and `docs/`.
- Binaries and packages: `humanityd`, `humanity`, `humanity-keyd`, `humanity-util`, and `humanity-pro*.deb`.
- Build and genesis names: `HUMANITY_UTIL_EXECUTABLE_NAME`, `HUMANITY_ROOT_KEY`, and `humanity_genesis.json`.
- Test and docs paths: `humanityd_*`, `humanity_util_*`, `humanity_keyd_*`, `docs/01_humanityd/`, `docs/02_humanity/`, and `docs/03_humanity-keyd/`.

Contract accounts (`ra`, `ra.token`, `ra.system`, `ra.claim`, and the rest) and the symbol **RA** are this protocol's names. They are not the previous repo's product title. Do not rename them as part of a blind search-and-replace.

A binary rename touches every test, doc, script (`scripts/launch-devnet.py`), and operator habit. Do that only after the questions below are answered.

**Decisions:** Rename the full product and operational surface. Use `humanityd`, `humanity`, `humanity-keyd`, and `humanity-util`; use `HUMANITY_ROOT_KEY`, `humanity_genesis.json`, and `humanity-pro*.deb`. Rename product copy, comments, binaries, CMake, packages, tests, scripts, docs paths, the root-key cache variable, and the genesis filename. Keep every existing `ra.*` contract account and the `RA` symbol unchanged.

### Completeness

- A search of the agreed scope finds no former product title.
- Names kept on purpose (`ra.*`, RA, and any binary the decision keeps) still match the Decisions paragraph.
- The build emits the agreed binary names, and `scripts/launch-devnet.py` starts a node with those names.
- History lists every renamed file and every name that was kept.

### Open questions

- How far does "all" go: docs and comments only, or binaries and CMake (`humanityd`, `humanity`, `humanity-keyd`, `humanity-util`, `HUMANITY_ROOT_KEY`, `humanity_genesis.json`, `humanity-pro*.deb`) as well?
- If binaries change, what are the new names?
- Do `ra.*` account names and the RA symbol stay?

### History

- 2026-10-27 — Filed from the protocol audit. No code change. GitHub repo and folder were already `Humanity-Pro`; product copy still used the former title.
- 2026-10-27 — Full rename implemented; status remains in progress because the binary build check is blocked before first-party sources compile. Renamed every file under `programs/channeld/` → `programs/humanityd/`, `programs/chan/` → `programs/humanity/`, `programs/keyd/` → `programs/humanity-keyd/`, `programs/channel-util/` → `programs/humanity-util/`, `docs/01_channeld/` → `docs/01_humanityd/`, `docs/02_chan/` → `docs/02_humanity/`, and `docs/03_keyd/` → `docs/03_humanity-keyd/`. Also renamed `CMakeModules/channel-config.cmake.in`, `genesis/channel_genesis.json`, `docs/channel_components.png`, both CLI completion files and their program copies, `plugins/channel-make_new_plugin.sh`, `tests/PerformanceHarness/ChanneldPluginArgs/` and its generator, every `tests/channeld_*` file, both `tests/channel_util_*` files, and `tests/keyd_auto_launch_test.py` to their decided Humanity Pro names. Removed six tracked CMake-generated C++ artifacts that embedded one developer's absolute checkout path; their portable `.in` templates remain the source of truth. Updated product copy, identifiers, paths, packaging, CI, scripts, tests, metrics, comments, and cryptographic chain-kind names throughout first-party files. Kept all `ra.*` account names and the `RA` symbol; also kept upstream `eosio`/`appbase` APIs, generic communication-channel wording, and external `channel-plugins` URL slugs because they are not product names. Checks: first-party former-title and former-binary search passed; `ra.*`/RA check passed; Python compile, workflow YAML parse, devnet `--help`, CMake configure, renamed-target enumeration, diff check, lints, and submodule-clean check passed. Native build did not emit binaries: x86 builds fail in the unmodified `bls12-381` submodule's ELF assembly on Mach-O, while arm64 gets past BLS but AppleClang 14 fails on the unmodified `bn256` submodule's `_BitInt`; therefore an actual `scripts/launch-devnet.py` node start could not run.

## HP-02 — Fix `ra.bpay` reward distribution so an inactive producer cannot hang the transfer

**Status:** in progress

### Context

`ra.system::claimrewards` still pays a producer directly from the `ra.bpay` balance (`contracts/ra.system/src/producer_pay.cpp`). Transfers **from** `ra` into `ra.bpay` are ignored on purpose so that funding path is not double-counted (`contracts/ra.bpay/src/ra.bpay.cpp`).

Any other RA transfer into `ra.bpay` walks the `prototalvote` index and records a share on the `rewards` table. The loop is:

```44:53:contracts/ra.bpay/src/ra.bpay.cpp
    while (true) {
        if (prod == idx.end()) break;
        if (prod->is_active == false) continue;

        top_producers.push_back(prod->owner);

        if (top_producers.size() == producer_count) break;

        prod++;
    }
```

`continue` does not advance `prod`. The first inactive producer spins until CPU runs out. If `top_producers` is empty, `quantity / top_producers.size()` is a divide by zero. Integer division also drops a remainder on the contract with no later sweep.

`claimrewards` on `ra.bpay` pays that table out. It is a different action from `ra.system::claimrewards`.

**Decisions:** Keep the existing `rewards` table for HP-02; HP-03 may redesign the fee sink separately. Divide evenly among the selected active producers and leave any indivisible remainder on `ra.bpay` rather than favoring one producer.

### Completeness

- A RA transfer to `ra.bpay` when `prototalvote` traversal reaches an inactive producer succeeds and skips that account.
- A transfer when no active producer exists fails on a check. It does not divide by zero or burn the CPU limit.
- The remainder matches the decision: it stays on `ra.bpay`, or the test shows who received it.
- A transfer from `ra` still does not write the `rewards` table.

### Open questions

- Should the unpaid remainder stay on `ra.bpay` until the next transfer, or go to the last producer?
- Is the `rewards` table still the right sink once HP-03 changes who gets fees?

### History

- 2026-10-27 — Filed from the audit of `contracts/ra.bpay/src/ra.bpay.cpp`. No code change.
- 2026-10-27 — Recorded the decisions to keep `rewards` and leave integer remainder on `ra.bpay`. Updated `on_transfer` so every producer-table iteration advances and an empty active set fails with `no active producers` before division. Added `unittests/ra.bpay_tests.cpp` for ignored `ra` funding, inactive-producer skipping, remainder accounting, and no-active rollback; extracted the existing core-contract loader to `unittests/core_contracts.hpp`, and corrected dependent return types in `unittests/eosio_system_tester.hpp` so the test harness parses under C++20. CMake configure and the new test source's syntax compile passed. Status remains in progress because this host only has eosio.cdt 1.8.1 rather than the required CDT 4.1.1, and the native unit-test binary is still blocked by the unmodified BLS/bn256 submodule toolchain issues recorded under HP-01, so the four chain checks have not run.

## HP-03 — Pay producers and owed work from activity fees, not from new RA inflation

**Status:** open

### Context

`PURE-LIQUID.md` says half of Flex activity fees and half of systemic-pool fees pay producers and approved work. The other half is holder income and a deeper vault. The game is not "print to pay the machines."

What the code does instead:

- `ra.system::claimrewards` computes `continuous_rate` inflation and `issue`s new RA, then splits it to savings, `ra.bpay`, and per-vote pay (`contracts/ra.system/src/producer_pay.cpp`).
- `ra.fees::on_transfer` holds RA. It calls `donatetorex` only when `rex_available()` is true (`contracts/ra.fees/src/ra.fees.cpp`). REX actions all hit `assert_rex_disabled()` first, so a normal chain never fills that pool. There is no action that pays producers or `ra.org` from `ra.fees`.
- `flex.token` taxes transfers into `reflection_pool`, `burn_pool`, and `project_pool`. `collectpool` sends swap fees to a chosen recipient or `project_account`. Nothing splits those amounts in half, and nothing notifies `ra.fees` or `ra.bpay`.
- `ra.org` can trickle a buck token to people the org owes. It is not wired to protocol fees.

REX stays off. Do not re-enable it to make `donatetorex` succeed.

### Completeness

- A covered fee inflow pays the agreed half to producers and owed work. The test shows both balances.
- The other half remains with holders or the vault. The test shows that balance too.
- The producer-pay path for this fee does not `issue` new RA.
- A REX action still aborts with the disabled check.
- RA already on `ra.fees` ends where the decision says it ends.

### Open questions

- Which inflows count as the fee half: RAM and name-bid only, Flex tax, vault collect, or all of them?
- Does inflationary `claimrewards` stop entirely, or only the part that overlaps this fee?
- Is owed work always `ra.org`, or is there another payee?
- What happens to RA already sitting on `ra.fees`?

### History

- 2026-10-27 — Filed from the audit of `ra.fees`, `producer_pay.cpp`, and `flex.token`. No code change.

## HP-04 — Make a Pure Liquid token actually locked ranged liquidity for its whole supply

**Status:** open

### Context

`WHITEPAPER.md` and `PURE-LIQUID.md` define Pure Liquid as: the entire maximum supply starts as the token side of one or more locked price ranges; circulation is someone buying out of that range; redemption is selling back; the lock can be extended and cannot be shortened.

`flex.token` today:

- `forge` records a max supply. `mint` issues any amount up to that max to the issuer (`contracts/ra.pure/flex.token.cpp`). Nothing requires those units to sit in a vault.
- `openpool`, `seedpool`, and `collectpool` send `createpool`, `deposit`, `addliquid`, `lockpos`, and `collect` to `swap_account()`, which defaults to `swap.alcor` (`contracts/ra.pure/PERMISSIONS.md`, `alcor-exchange/alcorswap_interface.hpp`). This repo has no ranged AMM. On a Humanity Pro chain that account does not exist unless someone deploys one and `setswap` points at it.
- `subliquid` and `transferpos` are not exposed. The external lock is what actually rejects an early pull. This contract does not store a rule that the position is the whole supply.
- Listing a twin because people locked inventory on the **native** chain is not implemented. `ra.claim` credits are trusted amounts, not a listing vote.
- `currency_stats` and `settings` in `contracts/ra.pure/flex.token.hpp` still use `EOSLIB_SERIALIZE`. New tables must not. Changing those two rows is an ABI change; do it only with a migration plan.

### Completeness

- After forge, token supply equals the units seated in locked ranges. A test reads both.
- A mint of units that are not in a locked range fails.
- Selling the token back returns the counter-asset from the range.
- A privileged action cannot set `unlock_time` earlier than the stored lock.
- The tests run against the swap this repo builds or configures. They do not call XPR `swap.alcor`.

### Open questions

- Does the ranged AMM live in this repo, or is an external contract deployed beside it and only interfaced here?
- One range or several bands per token?
- Who may extend a lock, and is there a maximum extension?
- How does native-chain inventory become the vote that lists a twin: a relayer proof (HP-06), a transfer into a contract, or something else?

### History

- 2026-10-27 — Filed from the audit of `contracts/ra.pure/`. No code change. Pool actions are an Alcor client, not a vault invariant.

## HP-05 — Let a holder opt out of the activity tax

**Status:** open

### Context

`PURE-LIQUID.md` lists opt-out as part of Flex: tax into a pool, splash to holders, chosen reward token, inheritance, opt out.

`setexempt` is an admin flag (`flex.token` authority) so a market account can skip the tax. `renounce` bans an account. A holder cannot turn the tax off for their own transfers. `interestoken`, `inheritance`, and `inheritmemo` choose where a share goes; they do not decline the tax.

### Completeness

- After a holder opts out, their transfer leaves reflection, burn, and project pools unchanged.
- `reflect` skips an opted-out balance, or pays it, exactly as the decision says. The test shows the balances.
- Opting back in restores the tax on the next transfer.
- An admin `setexempt` account still skips the tax. A non-admin call to `setexempt` fails.

### Open questions

- Does opt-out also refuse incoming reflections, or only the tax on the way out?
- Is opt-out per token symbol or for the whole account?
- Can an opted-out account still set an inheritance tree?

### History

- 2026-10-27 — Filed from the audit of `flex.token` actions. No code change.

## HP-06 — Replace trusted relayer credit with on-chain deposit proofs

**Status:** open

### Context

`ra.claim` is deposit-there / claim-here. A relayer calls `credit` or `creditopen`. The user calls `claim`, `claimsig`, or `claimopen`. `contracts/ra.claim/FUTURE.md` says this is not Wire: no headers, receipts, state proofs, outposts, or light clients. Relayers are rotated with `addrelayer` / `rmrelayer`. The treasury must already hold the RA.

`claimsig` and `claimopen` prove the **user** key. They do not prove the external deposit happened.

### Completeness

- `credit` with no valid proof fails, and the treasury balance is unchanged.
- One valid proof credits the recipient once. The same proof a second time fails.
- `claim`, `claimsig`, or `claimopen` pays that credit once and does not pay it again.
- A relayer account with no proof cannot create a deposit row.

### Open questions

- Which external chains are in the first proof (EVM log, Antelope action trace, or both)?
- Who posts the headers, and how many confirmations are required?
- Does a failed proof leave the treasury untouched?
- Is the relayer path removed or kept as a break-glass?

### History

- 2026-10-27 — Filed from `contracts/ra.claim/FUTURE.md` and `ra.claim.cpp`. Signed claim paths exist. Proving does not. No code change.

## HP-07 — Add non-aborting key recovery and a contract-readable permission read

**Status:** open

### Context

`FUTURE.md` lists two host gaps before a richer identity layer: Wire's non-aborting `try_recover_key`, and a contract-readable `get_permission`. Today `linksig`, `claimsig`, and `claimopen` call `recover_key`, which fails the transaction on a bad signature. A contract cannot read an account's permission to see which keys are already installed.

EM and ED already work when `EM_ED_KEYS` is active. `recover_key` checks an ED signature over the lowercase hex of a 32-byte digest. Stock CDT `eosio::signature` has no EM/ED alternative, so the contracts pass packed signature bytes (`contracts/ra.authex/include/ra.authex/recover.hpp`).

This is host work in the node, then a contract change to use it. It is not required for v1 relayer claims.

### Completeness

- A bad signature returns a mismatch and the action can continue. Tables written before the attempt are unchanged.
- A good signature recovers the same packed key as `recover_key` for EM and for ED.
- A contract read of an account permission returns that permission's keys and threshold.
- A test covers the mismatch path and the successful read.

### Open questions

- Is this in scope before HP-06, or only when a contract needs to try several keys in one action?
- Should the new intrinsics match Wire's names and argument layout?

### History

- 2026-10-27 — Filed from `contracts/ra.claim/FUTURE.md`. No code change.

## HP-08 — Social recovery: unusual or large transfers need upstream confirmation

**Status:** open

### Context

`WHITEPAPER.md` section 5: the user keeps their keys. A large transfer, or one that does not look like them, needs people **upstream** (those who invited and vouched) to confirm. The graph fades without attention. The paper says the object that stores the graph is the Passport (HP-12).

No contract stores invite edges, transfer limits, or a pending transfer that waits on upstream signatures. `ra.msig` is the stock multisig proposal tool. It is not this graph.

### Completeness

- A transfer under the limit moves the tokens in that action.
- A transfer over the limit stays pending. The sender's balance and the recipient's balance stay put until the agreed upstream set confirms.
- An upstream account past the fade window cannot confirm. A confirmation from outside the set fails.
- The owner's active key still signs ordinary transfers. No key is copied onto a guardian account.

### Open questions

- What is "does not look like you": size only, new recipient, or both?
- How many upstream confirmations, and what is the timeout if they never sign?
- Does this wrap `ra.token::transfer`, or is it a separate vault the user opts into?
- Can HP-08 start with an explicit guardian list before Passport fading exists?

### History

- 2026-10-27 — Filed from the whitepaper. No contract exists. No code change.

## HP-09 — Time-based daily RA for attention, not a new inflation print

**Status:** open

### Context

`WHITEPAPER.md` section 2 and the Tetra section: claims are stamped to a person and an interval. Daily RA is spent on offers. You cannot mint two days of influence in one second. RA is redeemable for attention in Discovery, and getting attention pays RA. The companion paper says income is a fee on movement, not a print.

`ra.token` is a standard token. There is no per-person interval, no daily balance, and no attention receipt. Producer inflation in `producer_pay.cpp` is a different print (HP-03).

### Completeness

- The first claim in an interval credits the agreed amount from the agreed source. The test shows the person's balance and the source balance.
- A second claim in that same interval fails.
- A claim in the next interval succeeds. A skipped interval pays once for the new interval, unless the decision says otherwise, and the test shows that amount.
- If the source is fees, RA `supply` does not increase. If the source is a capped schedule, `supply` stays at or under the cap.

### Open questions

- Where do the units come from: a share of fees, a capped schedule, or both?
- What is the interval (calendar day, 24 hours from the last claim)?
- Who is "a person" before Passport and Recurve exist: any account, or only a verified one?
- Does unspent daily RA expire?

### History

- 2026-10-27 — Filed from the whitepaper. No code change.

## HP-10 — Weight proposals by a verified person, then activity, then a living graph

**Status:** open

### Context

`WHITEPAPER.md`: who is owed, and which proposals pass, is public. Weight starts with a verified person, then activity on this chain, then a living social graph. A large RA stack adds only a little. Whale stake does not buy the room.

`ra.system` voting is still stake-weighted producer voting (`contracts/ra.system/src/voting.cpp`). `ra.bpay`'s extra distribution also ranks producers by `prototalvote`. Nothing in the tree scores a person, CPU actually used, or a fading graph.

### Completeness

- Two equal people with equal activity tie, including when one holds far more RA. The test shows the weights.
- Adding the agreed RA term moves the result only by that term. A whale does not flip the outcome alone.
- An edge past the fade window is absent from the weight.
- The producer schedule path matches the decision: it uses this weight, or the old stake vote is still the one the test shows.

### Open questions

- Does this replace producer voting, or only govern proposals and who is owed?
- How is "activity" measured: CPU billed, transfers, offers completed?
- How little may a large RA stack add (a cap, a log, a fixed bonus)?
- What verifies the person before HP-14 exists?

### History

- 2026-10-27 — Filed from the whitepaper against `voting.cpp`. No code change.

## HP-11 — Offers: an action, a RA cost or payment, and a check that it was done

**Status:** open

### Context

`WHITEPAPER.md` section 6: Tetrans spend daily RA on offers. An offer is an action, a cost or a payment in RA (or none), and a way to know it was done. Connections form when offers are completed. No offer table, escrow, or completion check exists under `contracts/`.

### Completeness

- Post, accept, and complete move RA only as the offer states. The test shows payer and receiver balances before and after.
- Complete without the agreed proof fails, and RA has not moved to the worker.
- An offer with zero RA still records completion.
- Another contract can read that completion by offer id.

### Open questions

- Who may post an offer: any account, or only a Passport?
- What proves "done": the counterparty, a set of witnesses, or a specific contract callback?
- Does the RA come from the daily balance (HP-09) or from a normal `ra.token` balance?

### History

- 2026-10-27 — Filed from the whitepaper. No code change.

## HP-12 — Passport: one record per human, stamps, accolades, connections that fade

**Status:** open

### Context

`WHITEPAPER.md`: Passport is who you are, where you are, what you offer, stamps, and accolades. One per human. Connections form when you complete offers, elect, and upvote. They fade if you vanish. This graph is the upstream for social recovery (HP-08) and the base of honest weight (HP-10).

No Passport contract exists. `ra.authex` links keys to an account. It does not say the account is one human, and it does not store stamps or fading edges.

### Completeness

- A second live Passport for the same human fails. The first row is unchanged.
- A stamp and an accolade append. Earlier stamps remain on the row.
- A connection past the fade window reads as not live.
- Another contract reads one connection by its key and gets live or not live. The call does not walk every edge.

### Open questions

- What stops a second Passport: a Recurve oath (HP-14), a guardian vote, or an admin until those exist?
- What is stored on the Passport versus only as a stamp hash?
- After how long without attention does a connection stop counting?

### History

- 2026-10-27 — Filed from the whitepaper. No code change.

## HP-13 — Discovery: regional, then national, then global attention charts

**Status:** open

### Context

`WHITEPAPER.md`: Discovery is daily charts of people, offers, and work. Regional first, then national, then global. RA is liquid for attention, and organic attention pays RA. There is no chart table, region id, or attention receipt in `contracts/`.

### Completeness

- One attention event changes that region's rank for that day and leaves the global chart unchanged.
- The agreed promotion action is what copies a result onto the next wider chart.
- RA paid for the event matches the agreed source and amount. The test shows both balances.
- A second event the same day updates that day's chart. It does not open a second day.

### Open questions

- What event counts as attention: an upvote, a completed offer, or a separate attest?
- Who pays the RA: the viewer, the daily pool, or a fee share?
- How is a region identified on chain?

### History

- 2026-10-27 — Filed from the whitepaper. No code change.

## HP-14 — Recurve: small-room elections that put an oath on the record

**Status:** open

### Context

`WHITEPAPER.md`: already-verified people meet a new person in a small room. An oath goes on the record. That is how a key becomes a human. This is the verification step Passport, daily RA, and human weight are waiting on. No election or oath contract exists.

### Completeness

- A room of the agreed size records the oath and sets the human flag or Passport.
- A room with fewer signers fails and writes no oath row.
- A signer who is not already verified is rejected.
- The stored oath payload matches the submitted text, hash, or both, as decided.

### Open questions

- How many verified people are in a room, and must they be face-to-face witnesses or is on-chain signature enough?
- What is the oath payload (text, hash, both)?
- Can an oath be revoked, and by whom?

### History

- 2026-10-27 — Filed from the whitepaper. No code change.

## HP-15 — Localize: a region turns on when people stake and found it

**Status:** open

### Context

`WHITEPAPER.md`: a region turns on when people stake and found it. Elected leaders set house rules and roles inside global bounds. Gatherings and places on a map. No region, stake-to-found, or house-rule contract exists. `ra.system` name bidding and producer voting are not this.

### Completeness

- Founding with the stake or the founder set short fails and creates no region.
- Founding with both met creates the region, and the stake is locked where the decision says.
- A leader's house rule inside the global bounds is stored.
- A house rule that crosses a global bound fails. A non-leader's rule fails.

### Open questions

- What is staked: RA, a Pure Liquid token, or a region-specific token?
- How are leaders chosen: Recurve rooms, Passport weight, or a local vote?
- Are map places coordinates on chain or a content hash?

### History

- 2026-10-27 — Filed from the whitepaper. No code change.

## HP-16 — Carnivals: a three-month season whose accolades land on the Passport

**Status:** open

### Context

`WHITEPAPER.md`: three months of competition, meetings, and a short vote at the end. Accolades land on the Passport. Depends on Passport (HP-12) existing as a place to write the accolade. No season clock or carnival vote exists.

### Completeness

- Opening a season stores the start and the end three months later, on the clock the decision chose.
- A vote inside the window writes the accolade on the Passport. A read of that Passport shows it.
- A vote before the start or after the end fails, and the Passport is unchanged.
- An account outside the agreed voter set cannot cast the final vote.

### Open questions

- Is the season a fixed calendar quarter or a 90-day span from the start action?
- Who may open a carnival, and who may vote at the end?
- Does an accolade change weight (HP-10) or is it only a stamp?

### History

- 2026-10-27 — Filed from the whitepaper. No code change.

## HP-17 — Chain tests for `ra.org`, `ra.resources`, and `flex.token`

**Status:** open

### Context

`unittests/ra.claim_tests.cpp` exercises `ra.authex` and `ra.claim` when contracts are built. `ra.org`, `ra.resources`, and `flex.token` are deployed by `scripts/launch-devnet.py` and have no behavior tests. `tests/interface/test_deploy_surface.py` only checks that `flex.token` does not expose `subliquid`, `transferpos`, or `burn`.

`ra.org` has `setconfig`, roles, grant, review, `closeperiod`, and an incoming-transfer trickle (`contracts/ra.org/src/ra.org.cpp`). `ra.resources` has plans, `buyplan`, expiry `process`, and memo `fund`. Those paths can regress with no failing test.

### Completeness

- `ra.org`: a review inside the window and `closeperiod` increase `owed`. A review outside the window fails.
- `ra.resources`: `buyplan` delegates the plan's CPU and NET. `process` after expiry undelegates. An unknown plan fails.
- `flex.token`: a taxed transfer moves the configured cut into the reflection pool, and `reflect` pays holders in proportion to balance. An unauthorized `setconfig` fails.
- All three run from the repo test harness (`ctest` or `tests/`). A one-off script is not the check.

### Open questions

- Prefer Boost tests beside `unittests/ra.claim_tests.cpp`, or Python tests under `tests/`?
- For `flex.token`, is a fake swap contract in the test enough until HP-04 has a real AMM?

### History

- 2026-10-27 — Filed from the audit of `unittests/` and `tests/`. No code change.
