from binance_data import prepare_informer_input
from informer_model import process_informer_input

try:
    # Prepare Informer input for Bitcoin with a 1-hour timeframe
    informer_input = prepare_informer_input("Bitcoin", "1h")
    # Check if input preparation was successful
    if informer_input:
        # Process input through the Informer model to get prediction and recommendation
        result = process_informer_input(informer_input)
        # Check if processing was successful
        if result:
            # Print the predicted price and recommendation
            print(f"Predicted price for {result['timeframe']}: {result['predicted_price']:.2f}")
            print(f"Recommendation: {result['recommendation']}")
        else:
            # Log failure to process input
            print("Failed to process Informer input.")
    else:
        # Log failure to prepare input
        print("Failed to prepare Informer input.")
except Exception as e:
    # Print any exceptions during execution
    print(f"Error: {str(e)}")