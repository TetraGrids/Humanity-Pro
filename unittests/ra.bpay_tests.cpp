#include <eosio/chain/abi_serializer.hpp>

#include <boost/test/unit_test.hpp>

#include <core_contracts.hpp>
#include <eosio_system_tester.hpp>

using namespace eosio;
using namespace eosio::chain;
using namespace eosio::testing;
using namespace eosio_system;
using namespace fc;

struct bpay_tester : eosio_system_tester<validating_tester> {
   bpay_tester() {
      core_contract = load_core_contract( *this, "ra.bpay"_n, "ra.bpay" );
      produce_block();

      if ( core_contract ) {
         const auto& account = control->db().get<account_object, by_name>( "ra.bpay"_n );
         abi_def abi;
         BOOST_REQUIRE( abi_serializer::to_abi( account.abi, abi ) );
         bpay_abi.set_abi( std::move( abi ), abi_serializer::create_yield_function( abi_serializer_max_time ) );
      }
   }

   base_tester::action_result transfer_to_bpay( const name& from, const asset& quantity ) {
      action transfer;
      transfer.account = "ra.token"_n;
      transfer.name    = "transfer"_n;
      transfer.data    = token_abi_ser.variant_to_binary(
         token_abi_ser.get_action_type( transfer.name ),
         mvo()( "from", from )( "to", "ra.bpay" )( "quantity", quantity )( "memo", "fund" ),
         abi_serializer::create_yield_function( abi_serializer_max_time ) );
      return base_tester::push_action( std::move( transfer ), from.to_uint64_t() );
   }

   asset reward( const name& owner ) {
      const auto data = get_row_by_account( "ra.bpay"_n, "ra.bpay"_n, "rewards"_n, owner );
      return data.empty() ? asset( 0, symbol( CORE_SYMBOL ) )
                          : bpay_abi.binary_to_variant( "rewards_row", data,
                                                        abi_serializer::create_yield_function( abi_serializer_max_time ) )["quantity"]
                               .as<asset>();
   }

   bool           core_contract = false;
   abi_serializer bpay_abi;
};

BOOST_AUTO_TEST_SUITE( ra_bpay_tests )

BOOST_AUTO_TEST_CASE( inactive_producers_and_remainder ) try {
   bpay_tester chain;
   if ( !chain.core_contract ) {
      BOOST_TEST_MESSAGE( "skip: ra.bpay wasm not built (configure -DBUILD_CONTRACTS=ON)" );
      return;
   }

   const auto producers = chain.active_and_vote_producers();
   BOOST_REQUIRE_EQUAL( chain.success(), chain.transfer_to_bpay( "ra"_n, core_from_string( "2.0000" ) ) );
   for ( const auto& producer : producers ) {
      BOOST_REQUIRE_EQUAL( asset( 0, symbol( CORE_SYMBOL ) ), chain.reward( producer ) );
   }

   BOOST_REQUIRE_EQUAL( chain.success(),
                        chain.push_action( producers.front(), "unregprod"_n,
                                           mvo()( "producer", producers.front() ) ) );

   BOOST_REQUIRE_EQUAL( chain.success(),
                        chain.transfer_to_bpay( "alice1111111"_n, core_from_string( "1.0001" ) ) );
   BOOST_REQUIRE_EQUAL( asset( 0, symbol( CORE_SYMBOL ) ), chain.reward( producers.front() ) );

   asset distributed( 0, symbol( CORE_SYMBOL ) );
   for ( size_t i = 1; i < producers.size(); ++i ) {
      const auto amount = chain.reward( producers[i] );
      BOOST_REQUIRE_EQUAL( core_from_string( "0.0500" ), amount );
      distributed += amount;
   }
   BOOST_REQUIRE_EQUAL( core_from_string( "1.0000" ), distributed );
   BOOST_REQUIRE_EQUAL( core_from_string( "3.0001" ), chain.get_balance( "ra.bpay"_n ) );

   for ( size_t i = 1; i < producers.size(); ++i ) {
      BOOST_REQUIRE_EQUAL( chain.success(),
                           chain.push_action( producers[i], "unregprod"_n,
                                              mvo()( "producer", producers[i] ) ) );
   }

   const auto sender_balance = chain.get_balance( "alice1111111"_n );
   const auto bpay_balance   = chain.get_balance( "ra.bpay"_n );
   BOOST_REQUIRE_EQUAL( chain.wasm_assert_msg( "no active producers" ),
                        chain.transfer_to_bpay( "alice1111111"_n, core_from_string( "0.1000" ) ) );
   BOOST_REQUIRE_EQUAL( sender_balance, chain.get_balance( "alice1111111"_n ) );
   BOOST_REQUIRE_EQUAL( bpay_balance, chain.get_balance( "ra.bpay"_n ) );
   BOOST_REQUIRE_EQUAL( core_from_string( "0.0500" ), chain.reward( producers.back() ) );
} FC_LOG_AND_RETHROW()

BOOST_AUTO_TEST_SUITE_END()
