// SPDX-License-Identifier: MIT

pragma solidity 0.8.19;

interface IERC20 {
    
    event Transfer(address indexed from, address indexed to, uint256 indexed amount);
    event Approval(address indexed owner, address indexed spender, uint256 indexed amount);

    function name() external view returns (string memory);
    function symbol() external view returns (string memory);
    function decimals() external view returns (uint8);
    function totalSupply() external view returns (uint256);
    function balanceOf(address account) external view returns (uint256);
    function allowance(address from, address spender) external view returns (uint256);
    function approve(address spender, uint256 amount) external returns (bool);
    function transfer(address to, uint256 amount) external returns (bool);
    function transferFrom(address from, address to, uint256 amount) external returns (bool);
}

/// @title Marketplace for ERC20 tokens
/// @author https://github.com/Krahjotdaan
/// @dev Open Source under MIT License
///
contract Marketplace {

    /// @notice struct of lot
    ///
    /// @param tokenAddress - address of ERC20 token
    /// @param tokenOwner - seller of this lot
    /// @param price - price per token unit
    /// @param amount - amount of token units
    ///
    struct Lot {
        address tokenAddress;
        address tokenOwner;
        uint256 price;
        uint256 amount;
    }

    /// @notice id of last lot
    uint256 public lotId;
    /// @notice contains all lots
    mapping(uint256 => Lot) public list;

    event ListLot(uint256 lotId, address owner, address tokenAddress, uint256 indexed price, uint256 indexed amount);
    event Cancel(uint256 lotId, uint256 indexed amount);
    event ChangePrice(uint256 lotId, uint256 indexed oldPrice, uint256 indexed newPrice);
    event Purchase(uint256 lotId, address tokenAddress, uint256 indexed price, uint256 indexed amount, address indexed customer);

    /// @notice function of putting an token up for sale
    ///
    /// @param _tokenAddress - address of ERC20 token
    /// @param _price - price per token unit
    /// @param _amount - amount of token units
    ///
    /// @dev calls functions allowance() and transferFrom() on _tokenAddress contract
    /// @dev causes interrupt if _tokenAddress is address(0) or not a contract
    /// @dev causes interrupt if _price or _amount is not over 0
    /// @dev causes interrupt if _amount is under then value of approved tokens to marketplace
    /// @dev causes interrupt if transfer of tokens to marketplace has failed
    ///
    function listLot(address _tokenAddress, uint256 _price, uint256 _amount) external returns(uint256) {

        require(_tokenAddress != address(0), "Marketplace: tokenAddress is address(0)");
        require(_tokenAddress.code.length > 0, "Marketplace: tokenAddress is not a contract");
        require(_price > 0, "Marketplace: price must be over 0");
        require(_amount > 0, "Marketplace: amount must be over 0");
        require(IERC20(_tokenAddress).allowance(msg.sender, address(this)) >= _amount, "Marketplace: not enough approved tokens to marketplace. Call function 'approve' to grant permission to marketplace to dispose of tokens");
        require(IERC20(_tokenAddress).transferFrom(msg.sender, address(this), _amount));

        ++lotId;
        list[lotId] = Lot(_tokenAddress, msg.sender, _price, _amount);

        emit ListLot(lotId, msg.sender, _tokenAddress, _price, _amount);

        return lotId;
    }

    /// @notice function of removal from sale of part of tokens in lot
    ///
    /// @param _id - id of lot from which part of tokens will be removed
    /// @param _amount - amount of tokens to be removed
    ///
    /// @dev if _amount is equal to amount of tokens in lot, lot will be deleted from list
    /// @dev calls function transfer() on token contract
    /// @dev causes interrupt if _amount <= 0 or _amount is more then amount of tokens in lot
    /// @dev causes interrupt if lot does not belong to someone who called this function
    ///
    function cancel(uint256 _id, uint256 _amount) external {

        require(_amount > 0, "Marketplace: amount must be over 0");

        Lot storage lot = list[_id];
        
        require(msg.sender == lot.tokenOwner, "Marketplace: this lot does not belong to you");
        require(lot.amount >= _amount, "Marketplace: too many tokens to cancel");
        require(IERC20(lot.tokenAddress).transfer(lot.tokenOwner, _amount));

        lot.amount -= _amount;

        if (lot.amount == 0) {
            delete list[_id];
        }
        
        emit Cancel(_id, _amount);
    }

    /// @notice function of changing price per token unit in lot
    ///
    /// @param _id - id of lot from which part of tokens will be removed
    /// @param newPrice - 1 token unit will be cost newPrice
    ///
    /// @dev causes interrupt if newPrice <= 0 or newPrice is equal to current price
    /// @dev causes interrupt if lot does not belong to someone who called this function
    ///
    function changePrice(uint256 _id, uint256 newPrice) external {
        require(newPrice > 0, "Marketplace: newPrice must be over 0");

        Lot storage lot = list[_id];
        
        require(lot.price != newPrice, "Marketplace: new price and current price must be different");
        require(msg.sender == lot.tokenOwner, "Marketplace: this lot does not belong to you");

        emit ChangePrice(_id, lot.price, newPrice);

        lot.price = newPrice;
    }

    /// @notice function of purchase of tokens
    ///
    /// @param _id - id of lot from which part of tokens will be purchased
    /// @param _amount - amount of token units that to someone who called this function wants to purchase
    ///
    /// @dev tranfers eth to seller and tokens to customer
    /// @dev if amount of eth passed to function is more then amount of tokens in lot * price per token unit, returns the difference between them to customer(change)
    /// @dev if _amount is equal to amount of tokens in lot, lot will be deleted from list
    /// @dev causes interrupt if _amount <= 0 or _amount is more then amount of tokens in lot
    /// @dev causes interrupt if amount of eth passed to function is less then amount of tokens in lot * price per token unit
    ///
    function purchase(uint256 _id, uint256 _amount) external payable {
        require(_amount > 0, "Marketplace: amount must be over 0");

        Lot storage lot = list[_id];

        require(msg.value >= lot.price * _amount, "Marketplace: not enough eth");
        require(lot.amount >= _amount, "Marketplace: too many tokens to purchase");
        require(IERC20(lot.tokenAddress).transfer(msg.sender, _amount));

        payable(lot.tokenOwner).transfer(lot.price * _amount);
        lot.amount -= _amount;

        if (msg.value > lot.price * _amount) {
            payable(msg.sender).transfer(msg.value - lot.price * _amount);
        }

        if (lot.amount == 0) {
            delete list[_id];
        }

        emit Purchase(_id, lot.tokenAddress, lot.price, _amount, msg.sender);
    }
}