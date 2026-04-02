---
description: 블록체인/Web3 개발. "블록체인", "Web3", "스마트 컨트랙트", "NFT", "토큰", "이더리움", "솔리디티" 트리거.
---

# 블록체인/Web3 개발

## 환경 설정
```bash
# Hardhat (추천)
npm install --save-dev hardhat @nomicfoundation/hardhat-toolbox
npx hardhat init

# Foundry (고급)
curl -L https://foundry.paradigm.xyz | bash
foundryup
```

## Solidity 스마트 컨트랙트

### ERC-20 토큰
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyToken is ERC20, Ownable {
    constructor(uint256 initialSupply) ERC20("MyToken", "MTK") Ownable(msg.sender) {
        _mint(msg.sender, initialSupply * 10 ** decimals());
    }

    function mint(address to, uint256 amount) public onlyOwner {
        _mint(to, amount);
    }

    function burn(uint256 amount) public {
        _burn(msg.sender, amount);
    }
}
```

### ERC-721 NFT
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract MyNFT is ERC721, ERC721URIStorage, Ownable {
    uint256 private _tokenIdCounter;
    uint256 public mintPrice = 0.01 ether;
    uint256 public maxSupply = 10000;

    constructor() ERC721("MyNFT", "MNFT") Ownable(msg.sender) {}

    function mint(string memory uri) public payable returns (uint256) {
        require(msg.value >= mintPrice, "Insufficient payment");
        require(_tokenIdCounter < maxSupply, "Max supply reached");

        uint256 tokenId = _tokenIdCounter;
        _tokenIdCounter++;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, uri);

        return tokenId;
    }

    function withdraw() public onlyOwner {
        payable(owner()).transfer(address(this).balance);
    }

    // Overrides
    function tokenURI(uint256 tokenId) public view override(ERC721, ERC721URIStorage)
        returns (string memory) {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId) public view override(ERC721, ERC721URIStorage)
        returns (bool) {
        return super.supportsInterface(interfaceId);
    }
}
```

### 마켓플레이스
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/IERC721.sol";
import "@openzeppelin/contracts/security/ReentrancyGuard.sol";

contract NFTMarketplace is ReentrancyGuard {
    struct Listing {
        address seller;
        address nftContract;
        uint256 tokenId;
        uint256 price;
        bool active;
    }

    mapping(uint256 => Listing) public listings;
    uint256 public listingCount;
    uint256 public platformFee = 250; // 2.5%

    event Listed(uint256 listingId, address seller, address nftContract, uint256 tokenId, uint256 price);
    event Sold(uint256 listingId, address buyer, uint256 price);
    event Cancelled(uint256 listingId);

    function list(address nftContract, uint256 tokenId, uint256 price) external returns (uint256) {
        require(price > 0, "Price must be > 0");

        IERC721(nftContract).transferFrom(msg.sender, address(this), tokenId);

        uint256 listingId = listingCount++;
        listings[listingId] = Listing({
            seller: msg.sender,
            nftContract: nftContract,
            tokenId: tokenId,
            price: price,
            active: true
        });

        emit Listed(listingId, msg.sender, nftContract, tokenId, price);
        return listingId;
    }

    function buy(uint256 listingId) external payable nonReentrant {
        Listing storage listing = listings[listingId];
        require(listing.active, "Not active");
        require(msg.value >= listing.price, "Insufficient payment");

        listing.active = false;

        uint256 fee = (listing.price * platformFee) / 10000;
        uint256 sellerAmount = listing.price - fee;

        payable(listing.seller).transfer(sellerAmount);
        IERC721(listing.nftContract).transferFrom(address(this), msg.sender, listing.tokenId);

        emit Sold(listingId, msg.sender, listing.price);
    }

    function cancel(uint256 listingId) external {
        Listing storage listing = listings[listingId];
        require(listing.seller == msg.sender, "Not seller");
        require(listing.active, "Not active");

        listing.active = false;
        IERC721(listing.nftContract).transferFrom(address(this), msg.sender, listing.tokenId);

        emit Cancelled(listingId);
    }
}
```

## Hardhat 설정
```typescript
// hardhat.config.ts
import { HardhatUserConfig } from "hardhat/config";
import "@nomicfoundation/hardhat-toolbox";
import * as dotenv from "dotenv";

dotenv.config();

const config: HardhatUserConfig = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL || "",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
    mainnet: {
      url: process.env.MAINNET_RPC_URL || "",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
  },
  etherscan: {
    apiKey: process.env.ETHERSCAN_API_KEY,
  },
};

export default config;
```

### 배포 스크립트
```typescript
// scripts/deploy.ts
import { ethers } from "hardhat";

async function main() {
  const [deployer] = await ethers.getSigners();
  console.log("Deploying with:", deployer.address);

  const MyNFT = await ethers.getContractFactory("MyNFT");
  const nft = await MyNFT.deploy();
  await nft.waitForDeployment();

  console.log("MyNFT deployed to:", await nft.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
```

```bash
# 배포
npx hardhat run scripts/deploy.ts --network sepolia

# 검증
npx hardhat verify --network sepolia DEPLOYED_ADDRESS
```

## 프론트엔드 연동

### Viem + Wagmi (추천)
```tsx
// wagmi.config.ts
import { createConfig, http } from 'wagmi';
import { mainnet, sepolia } from 'wagmi/chains';
import { injected, walletConnect } from 'wagmi/connectors';

export const config = createConfig({
  chains: [mainnet, sepolia],
  connectors: [
    injected(),
    walletConnect({ projectId: 'YOUR_PROJECT_ID' }),
  ],
  transports: {
    [mainnet.id]: http(),
    [sepolia.id]: http(),
  },
});

// 컴포넌트에서 사용
import { useAccount, useConnect, useDisconnect, useWriteContract } from 'wagmi';

function WalletConnect() {
  const { address, isConnected } = useAccount();
  const { connect, connectors } = useConnect();
  const { disconnect } = useDisconnect();

  if (isConnected) {
    return (
      <div>
        <p>Connected: {address}</p>
        <button onClick={() => disconnect()}>Disconnect</button>
      </div>
    );
  }

  return (
    <div>
      {connectors.map((connector) => (
        <button key={connector.id} onClick={() => connect({ connector })}>
          Connect {connector.name}
        </button>
      ))}
    </div>
  );
}

// 컨트랙트 호출
function MintNFT() {
  const { writeContract, isPending, isSuccess } = useWriteContract();

  const mint = () => {
    writeContract({
      address: '0x...',
      abi: MyNFTAbi,
      functionName: 'mint',
      args: ['ipfs://...'],
      value: parseEther('0.01'),
    });
  };

  return (
    <button onClick={mint} disabled={isPending}>
      {isPending ? 'Minting...' : 'Mint NFT'}
    </button>
  );
}
```

## IPFS/메타데이터
```typescript
import { create } from 'ipfs-http-client';

const ipfs = create({ url: 'https://ipfs.infura.io:5001/api/v0' });

async function uploadMetadata(name: string, description: string, imageUrl: string) {
  const metadata = {
    name,
    description,
    image: imageUrl,
    attributes: [
      { trait_type: 'Rarity', value: 'Common' },
    ],
  };

  const result = await ipfs.add(JSON.stringify(metadata));
  return `ipfs://${result.path}`;
}
```

$ARGUMENTS
