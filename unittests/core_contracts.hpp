#pragma once

#include <eosio/testing/tester.hpp>

#include <fc/io/fstream.hpp>

#include <filesystem>

inline bool load_core_contract( eosio::testing::base_tester& chain, const eosio::chain::name& account,
                                const std::string& stem ) {
#ifdef HUMANITY_PRO_CONTRACTS_DIR
   const std::string base = std::string( HUMANITY_PRO_CONTRACTS_DIR ) + "/" + stem + "/" + stem;
   if ( !std::filesystem::exists( base + ".wasm" ) || !std::filesystem::exists( base + ".abi" ) )
      return false;
   std::string wasm;
   std::string abi;
   fc::read_file_contents( base + ".wasm", wasm );
   fc::read_file_contents( base + ".abi", abi );
   chain.set_code( account, std::vector<uint8_t>( wasm.begin(), wasm.end() ) );
   chain.set_abi( account, abi );
   return true;
#else
   (void)chain;
   (void)account;
   (void)stem;
   return false;
#endif
}
