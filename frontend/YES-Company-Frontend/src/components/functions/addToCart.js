export const addToCart = (product_id, quantity, items, setItems) => {
  let existingItem = items.find((item) => item.product_id === product_id);
  if (!existingItem) {
    setItems([...items, { product_id, quantity: quantity }]);
  } else {
    // existingItem.quantity += quantity;
    // setItems([...items, existingItem]);
    // setItems((prevItems) =>
    //   prevItems.map((item) =>
    //     item.productId === productId
    //       ? { ...item, quantity: item.quantity + quantity }
    //       : item
    //   )
    // );
    // remember to create a new List so that React knows to update the state of that List
    let newItems = items.map((item) => {
      if (item.product_id === product_id) {
        return { ...item, quantity: item.quantity + quantity };
      } else {
        return item;
      }
    });
    setItems(newItems);
  }
};
