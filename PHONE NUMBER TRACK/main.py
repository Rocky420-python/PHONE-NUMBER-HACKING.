from cfonts import render
from phonenumbers import geocoder, carrier, timezone, region_code_for_number
from phonenumbers import parse, PhoneNumberFormat, format_number
from phonenumbers import carrier
from phonenumbers.phonenumberutil import (
    NumberParseException,
    is_valid_number,
    is_possible_number,
    number_type,
    PhoneNumberType
)
import sys
import re
import requests

# ─── Fancy Banner ───────────────────────────────────────────────
banner = render(
    "SPARKS MINDS",
    colors=["red", "yellow", "cyan"],
    align="center",
    font="block"
)

sub_banner = render(
    "ADVANCED PHONE OSINT v2.1",
    colors=["white", "grey"],
    align="center",
    font="tiny"
)

print(banner)
print(sub_banner)
print("═" * 65)

def get_number_type_name(ntype):
    types = {
        PhoneNumberType.MOBILE:         "Mobile",
        PhoneNumberType.FIXED_LINE:     "Fixed Line",
        PhoneNumberType.FIXED_LINE_OR_MOBILE: "Fixed/Mobile",
        PhoneNumberType.TOLL_FREE:      "Toll Free",
        PhoneNumberType.PREMIUM_RATE:   "Premium Rate",
        PhoneNumberType.SHARED_COST:    "Shared Cost",
        PhoneNumberType.VOIP:           "VoIP",
        PhoneNumberType.PERSONAL_NUMBER:"Personal Number",
        PhoneNumberType.PAGER:          "Pager",
        PhoneNumberType.UAN:            "UAN",
        PhoneNumberType.VOICEMAIL:      "Voicemail",
        PhoneNumberType.UNKNOWN:        "Unknown"
    }
    return types.get(ntype, "Not detected")

def clean_phone(phone_str):
    # Remove everything except digits and +
    return re.sub(r'[^0-9+]', '', phone_str.strip())

def advanced_phone_lookup():
    print("\n" + "─"*65)
    print("   Phone Number Intelligence Tool   ")
    print("─"*65)

    while True:
        raw = input("\nEnter phone number (or 'q' to quit): ").strip()

        if raw.lower() in ['q', 'quit', 'exit', '0']:
            print("\nGoodbye! Stay safe out there ✌️")
            sys.exit(0)

        phone = clean_phone(raw)

        if not phone:
            print("→ No number entered!")
            continue

        try:
            # Try to parse with default region = None (most strict)
            numobj = parse(phone, None)

            # More relaxed parsing attempts if failed
            if not is_possible_number(numobj):
                print("Trying more relaxed parsing...")
                numobj = parse(phone, "US")  # common fallback

            ip = requests.get('https://api.ipify.org').text

            print("\n" + "═"*65)

            # Basic information
            print(f"International format : {format_number(numobj, PhoneNumberFormat.E164)}")
            print(f"National format      : {format_number(numobj, PhoneNumberFormat.NATIONAL)}")
            print(f"International (no +) : {format_number(numobj, PhoneNumberFormat.INTERNATIONAL).replace('+','')}")

            print("-"*50)
            print(f"Country code         : +{numobj.country_code}")
            print(f"Region code (ISO)    : {region_code_for_number(numobj) or '—'}")
            print(f"Country / Region     : {geocoder.description_for_number(numobj, 'en') or '—'}")

            # Carrier & Type (most useful fields)
            carrier_name = carrier.name_for_number(numobj, "en")
            print(f"Current/Last Carrier : {carrier_name if carrier_name else '— (not found / ported?)'}")
            print(f"Line type            : {get_number_type_name(number_type(numobj))}")
            print(f"Mobaile Ip           : {ip}")

            # Timezones (usually very useful)
            tz = timezone.time_zones_for_number(numobj)
            print(f"Time zone(s)         : {', '.join(tz) if tz else '—'}")

            # Validation
            print("-"*50)
            print(f"Valid number         : {'Yes' if is_valid_number(numobj) else '✗ No'}")
            print(f"Possible number      : {'Yes' if is_possible_number(numobj) else '✗ No'}")


            # Extra info people love to see
            print("-"*50)
            print("Note:")
            print("• Carrier info is often outdated (number porting)")
            print("• Very few countries still provide precise location")
            print("• No public reliable phone → IP / exact GPS lookup exists anymore")

        except NumberParseException as e:
            print(f"\n✘ Parse error: {e}")
            print("Try formats like: +917428730894, +447311121710, +8801712345678")

        print("═"*65)

def main():
    print("\n" * 2)
    print("              Available Commands:")
    print("              ───────────────────")
    print("               number / n      → start lookup")
    print("               q / quit / exit  → exit program")
    print("               cls / clear      → clear screen\n")

    while True:
        cmd = input("sparks> ").strip().lower()

        if cmd in ["number", "n", "lookup", "start"]:
            advanced_phone_lookup()
        elif cmd in ["cls", "clear"]:
            print("\033c", end="")
            print(banner)
            print(sub_banner)
        elif cmd in ["q", "quit", "exit", "0"]:
            print("\nShutting down...\n")
            break
        else:
            print("Unknown command. Try: number / q / clear")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nCtrl+C detected. Goodbye! 👋")