# Finance RAG Chatbot Project

## Table of Contents

- [📍 Overview](#-overview)
- [👾 Features](#-features)
- [📁 Project Structure](#-project-structure)
  - [📂 Project Index](#-project-index)
- [🚀 Getting Started](#-getting-started)
  - [☑️ Prerequisites](#-prerequisites)
  - [⚙️ Installation](#-installation)
  - [🤖 Usage](#🤖-usage)
  - [🧪 Testing](#🧪-testing)
- [📌 Project Roadmap](#-project-roadmap)
- [🔰 Contributing](#-contributing)
- [🎗 License](#-license)
- [🙌 Acknowledgments](#-acknowledgments)

## 📍 Overview

Discover a dynamic project streamlining communication with an AI assistant for financial tasks. Seamlessly interact with 'Finbot' to search, summarize, and store information. Enhance productivity and engagement with a user-friendly chat interface. Simplify financial assistance through AI-driven conversations. Ideal for users seeking efficient task execution within a personalized chat environment.

---

## 👾 Features

|      | Feature         | Summary       |
| :--- | :---:           | :---          |
| ⚙️  | **Architecture**  | <ul><li>Utilizes a microservices architecture with services orchestrated using `docker-compose.yaml`. This allows for easy scaling and deployment.</li><li>Separation of concerns achieved through modular design with services like `Qdrant` and `Redis` in dedicated containers.</li><li>Centralized configuration management via `.env` files for seamless integration with external services.</li><li>Key language: `Python`</li></ul> |
| 🔩 | **Code Quality**  | <ul><li>Linting and code formatting enforced with tools like `flake8`, maintaining consistent coding standards across the project.</li><li>Unit tests implemented using `pytest` to ensure robustness and reliability of codebase.</li><li> CI/CD pipelines used for automated testing and deployment, enhancing code quality checks.</li><li>Integration with `poetry` for dependency management and virtual environment isolation.</li></ul> |
| 📄 | **Documentation** | <ul><li>Extensive documentation across codebase files with a primary focus on Python.</li><li>README files, inline comments, and docstrings provide clarity on code functionality and usage.</li><li>Usage of `markdown` for consistent formatting of documentation.</li><li>Documentation generated with `poetry` and `pip` for package management references.</li></ul> |
| 🔌 | **Integrations**  | <ul><li>Integration with key libraries like `OpenAI`, `Gradio`, `Playwright`, and `Requests` for AI capabilities, GUI development, web scraping, and HTTP requests.</li><li>Seamless interaction with external services like `Redis` and `Qdrant` for data storage and retrieval.</li><li>Utilizes `HTTPX` for efficient asynchronous HTTP requests within the project.</li><li>Integration with `docker` for containerized deployment and management.</li></ul> |
| 🧩 | **Modularity**    | <ul><li>Codebase organized into separate modules for different functionalities like `core`, `tasks`, `prompts`, and `vectordb` for easy maintenance and scalability.</li><li>Use of interfaces and abstract classes for defining clear boundaries between components.</li><li>Facilitates reusability and extensibility with components like `base.py` and `enum_type.py`.</li><li>Loosely coupled components ensuring flexibility and ease of modification.</li></ul> |
| 🧪 | **Testing**       | <ul><li>Comprehensive unit tests covering various components and functionalities to ensure code correctness.</li><li>Test cases written using `pytest` to validate expected behavior and edge cases.</li><li>Test-driven development approach followed for robust and reliable codebase.</li><li>Continuous testing and integration pipelines implemented for automated testing and feedback loop.</li></ul> |

---

## 📁 Project Structure

```sh
└── /
    ├── LICENSE
    ├── Makefile
    ├── README.md
    ├── apps
    │   ├── agent
    │   └── notebooks
    ├── docker-compose.yaml
    ├── images
    │   ├── chat.png
    │   ├── flow.png
    │   └── flow.svg
    ├── readmeai.md
    └── requirements.txt
```


### 📂 Project Index
<details open>
	<summary><b><code>/</code></b></summary>
	<details> <!-- __root__ Submodule -->
		<summary><b>__root__</b></summary>
		<blockquote>
			<table>
			<tr>
				<td><b><a href='/docker-compose.yaml'>docker-compose.yaml</a></b></td>
				<td>- Defines services, volumes, and networks for running Redis and Qdrant databases in separate containers<br>- Specifies port mappings, container names, and restart policies<br>- Creates a bridge network for communication<br>- This file orchestrates the setup of essential infrastructure components for the project.</td>
			</tr>
			<tr>
				<td><b><a href='/requirements.txt'>requirements.txt</a></b></td>
				<td>- Enabling seamless integration of OpenAI, Gradio, Playwright, HTTPX, Requests, and Redis dependencies within the project, the code file serves as a blueprint for managing essential libraries and modules<br>- Its purpose is to streamline the project's architecture by providing easy access and central management of key components.</td>
			</tr>
			<tr>
				<td><b><a href='/Makefile'>Makefile</a></b></td>
				<td>- Facilitates installation, updating, exporting dependencies, and running the application via predefined commands<br>- The Makefile streamlines the setup process by automating essential tasks to manage dependencies and launch the application seamlessly.</td>
			</tr>
			</table>
		</blockquote>
	</details>
	<details> <!-- apps Submodule -->
		<summary><b>apps</b></summary>
		<blockquote>
			<details>
				<summary><b>agent</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='/apps/agent/.env'>.env</a></b></td>
						<td>Define environment variables for the agent application to configure connections with external services like Redis, Qdrant, OpenAI, and Google APIs within the project architecture.</td>
					</tr>
					<tr>
						<td><b><a href='/apps/agent/.conda_config'>.conda_config</a></b></td>
						<td>Facilitates configuration settings for the 'fin-agent' application within the overall project architecture.</td>
					</tr>
					<tr>
						<td><b><a href='/apps/agent/requirements.txt'>requirements.txt</a></b></td>
						<td>- Define project dependencies and requirements in the Agent application through the 'requirements.txt' file<br>- This file lists specific versions of Python packages needed for the project.</td>
					</tr>
					<tr>
						<td><b><a href='/apps/agent/.env.example'>.env.example</a></b></td>
						<td>Define the required environment variables for the agent application to establish connections with Redis and QdRant services, along with API keys for OpenAI and Google services.</td>
					</tr>
					<tr>
						<td><b><a href='/apps/agent/pyproject.toml'>pyproject.toml</a></b></td>
						<td>- Facilitates dependency management, defining project metadata, and listing dev dependencies in the `pyproject.toml` file for the `finbot-agent` project<br>- Key libraries such as FastAPI, Gradio, Pydantic, and others are specified for the project's functionality and development environment<br>- This file plays a crucial role in organizing project dependencies and configurations.</td>
					</tr>
					<tr>
						<td><b><a href='/apps/agent/Makefile'>Makefile</a></b></td>
						<td>- The code file in 'apps/agent/Makefile' manages installing dependencies, checking code quality, linting, exporting requirements, building wheel files, cleaning artifacts, and fetching the main branch<br>- It provides essential commands for maintaining the project's code quality and packaging.</td>
					</tr>
					</table>
					<details>
						<summary><b>src</b></summary>
						<blockquote>
							<table>
							<tr>
								<td><b><a href='/apps/agent/src/main.py'>main.py</a></b></td>
								<td>- Implements a chatbot application using FastAPI and Gradio<br>- Handles conversations between users and the assistant, displaying chat history<br>- Redirects users to the demo interface and orchestrates the app's deployment via uvicorn.</td>
							</tr>
							</table>
							<details>
								<summary><b>gui</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/apps/agent/src/gui/demo.py'>demo.py</a></b></td>
										<td>- Implements a user-friendly chat interface with a conversational AI agent named Finbot<br>- Users can interact with Finbot to perform various tasks like searching URLs, summarizing content, and storing vectors<br>- The interface provides a seamless chat experience with message history and real-time updates.</td>
									</tr>
									</table>
									<details>
										<summary><b>style</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='/apps/agent/src/gui/style/style.css'>style.css</a></b></td>
												<td>Improve GUI layout by centering h2 headings in markdown content using the provided CSS styles.</td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
							<details>
								<summary><b>core</b></summary>
								<blockquote>
									<table>
									<tr>
										<td><b><a href='/apps/agent/src/core/agents.py'>agents.py</a></b></td>
										<td>- The code orchestrates user interactions, identifying tasks and determining appropriate responses<br>- It executes generic tasks, searches for information, and fetches URLs based on user input<br>- Additionally, it leverages a vector store for data storage and retrieval, enhancing the system's capabilities for task execution and user engagement within the project's architecture.</td>
									</tr>
									</table>
									<details>
										<summary><b>llms</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='/apps/agent/src/core/llms/openai.py'>openai.py</a></b></td>
												<td>- Enables asynchronous generation of chat completions using the OpenAI API, facilitating the creation of chat templates and interactions<br>- Implements a model instantiation and message processing for seamless communication between users and systems in the project's AI-driven chat feature.</td>
											</tr>
											<tr>
												<td><b><a href='/apps/agent/src/core/llms/base.py'>base.py</a></b></td>
												<td>Defines an abstract BaseModel class in the core module for handling queries.</td>
											</tr>
											</table>
										</blockquote>
									</details>
									<details>
										<summary><b>embeddings</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='/apps/agent/src/core/embeddings/openai.py'>openai.py</a></b></td>
												<td>- Facilitates asynchronous generation of embeddings for text strings using OpenAI API<br>- Defines an OpenAIEmbedding class that initializes model settings and handles embedding creation<br>- Offers methods to batch embed text and retrieve embedding dimensions based on OpenAI model configurations.</td>
											</tr>
											<tr>
												<td><b><a href='/apps/agent/src/core/embeddings/base.py'>base.py</a></b></td>
												<td>- Defines abstract classes for generating embeddings from text data<br>- The code outlines methods for embedding batches of text strings into numerical vectors, generating individual text embeddings, and obtaining the embedding dimension.</td>
											</tr>
											</table>
										</blockquote>
									</details>
									<details>
										<summary><b>shared</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='/apps/agent/src/core/shared/const.py'>const.py</a></b></td>
												<td>Define base headers and cache TTL settings for HTTP requests within the agent's core functionality.</td>
											</tr>
											</table>
										</blockquote>
									</details>
									<details>
										<summary><b>vectordb</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='/apps/agent/src/core/vectordb/qdrant.py'>qdrant.py</a></b></td>
												<td>- Manages interactions with Qdrant search engine for vector data storage and retrieval<br>- Provides methods for creating collections, batch insertion of points, and querying for similar embeddings<br>- Handles text extraction, UUID generation, and post-processing of query results<br>- Integration with OpenAI embeddings and Redis for efficient data operations.</td>
											</tr>
											<tr>
												<td><b><a href='/apps/agent/src/core/vectordb/base.py'>base.py</a></b></td>
												<td>- Define an abstract class for handling vector storage systems<br>- Methods allow for client retrieval, collection creation, batch and single data point insertion, and similarity querying within specified collections<br>- This class forms the foundation for integrating various vector storage systems into the project architecture.</td>
											</tr>
											</table>
										</blockquote>
									</details>
									<details>
										<summary><b>prompts</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='/apps/agent/src/core/prompts/generic.py'>generic.py</a></b></td>
												<td>Define a user-friendly template for responding to generic chat prompts, encouraging detailed queries to provide accurate and helpful responses.</td>
											</tr>
											<tr>
												<td><b><a href='/apps/agent/src/core/prompts/chat.py'>chat.py</a></b></td>
												<td>- The chat.py file in the project's agent core prompts module defines prompts for a virtual financial assistant called FinBot<br>- It sets communication guidelines, permissible tasks, and language preferences for the assistant to engage with users effectively<br>- The file establishes a friendly and professional tone while emphasizing the importance of thorough responses and using data to enhance credibility.</td>
											</tr>
											<tr>
												<td><b><a href='/apps/agent/src/core/prompts/task_check.py'>task_check.py</a></b></td>
												<td>Define user intents and determine tasks based on input while supporting various response formats.</td>
											</tr>
											<tr>
												<td><b><a href='/apps/agent/src/core/prompts/summarize.py'>summarize.py</a></b></td>
												<td>- Create concise summaries of conversations by extracting key information for precise Google searches, maintaining language consistency<br>- Minimize redundancy, eliminate explanations, datetime references, and unnecessary keywords from the output format.</td>
											</tr>
											<tr>
												<td><b><a href='/apps/agent/src/core/prompts/rag.py'>rag.py</a></b></td>
												<td>- Defines a prompt for the RAG (Red, Amber, Green) rating system in the agent application core<br>- The prompt includes contextual information for answering user questions, emphasizing the use of provided context without inventing additional details<br>- Good for guiding user responses within the app's guidelines and maintaining consistency.</td>
											</tr>
											</table>
										</blockquote>
									</details>
									<details>
										<summary><b>types</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='/apps/agent/src/core/types/enum_type.py'>enum_type.py</a></b></td>
												<td>- Define Enum types for OpenAI and text embedding models, along with a TaskType class for task categorization<br>- The code provides clear identifiers for different AI and embedding models, as well as functions to determine if a task is generic or not within the project's architecture.</td>
											</tr>
											</table>
										</blockquote>
									</details>
									<details>
										<summary><b>tasks</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='/apps/agent/src/core/tasks/generic.py'>generic.py</a></b></td>
												<td>- Implements a task executor that utilizes an OpenAI model to process input queries within the project's agent application<br>- The executor extends a base task class, allowing for the execution of generic tasks with flexibility in the choice of the underlying model.</td>
											</tr>
											<tr>
												<td><b><a href='/apps/agent/src/core/tasks/base.py'>base.py</a></b></td>
												<td>- Defines a base class for tasks in the codebase architecture<br>- Responsible for enforcing a consistent structure across task implementations by defining a method that must be implemented by subclasses<br>- This ensures tasks adhere to a specific interface within the project structure.</td>
											</tr>
											<tr>
												<td><b><a href='/apps/agent/src/core/tasks/rag.py'>rag.py</a></b></td>
												<td>- Implement a RAG task executor in the project's agent app core tasks<br>- It uses OpenAI models to process queries alongside context and history, generating responses through the RAG format<br>- This code enhances the project's ability to perform specialized tasks using AI models efficiently.</td>
											</tr>
											</table>
										</blockquote>
									</details>
									<details>
										<summary><b>crawler</b></summary>
										<blockquote>
											<table>
											<tr>
												<td><b><a href='/apps/agent/src/core/crawler/base.py'>base.py</a></b></td>
												<td>- The code file in apps/agent/src/core/crawler/base.py extracts and normalizes URLs from HTML content, prioritizing same-domain URLs<br>- It also converts HTML to markdown, cleaning up formatting<br>- This base crawler serves as a foundation for fetching data and converting it to markdown content.</td>
											</tr>
											<tr>
												<td><b><a href='/apps/agent/src/core/crawler/html.py'>html.py</a></b></td>
												<td>- The provided code file in apps/agent/src/core/crawler/html.py handles asynchronous web crawling functionalities, including fetching data via HTTP requests or a browser, caching data, and recursively collecting content from multiple URLs<br>- It employs asyncio, httpx, Playwright, and maintains cache and timeout configurations<br>- The code elegantly orchestrates data fetching strategies to optimize web scraping tasks within the project architecture.</td>
											</tr>
											</table>
										</blockquote>
									</details>
								</blockquote>
							</details>
						</blockquote>
					</details>
				</blockquote>
			</details>
			<details>
				<summary><b>notebooks</b></summary>
				<blockquote>
					<table>
					<tr>
						<td><b><a href='/apps/notebooks/tool.ipynb'>tool.ipynb</a></b></td>
						<td>- Summary:

The code file `tool.ipynb` in the `notebooks` directory imports tools from the `src.core.tools` module, setting up functionality for performing task checks, fetching URLs, and searching<br>- Additionally, it loads environment variables from the `agent/.env` file<br>- This notebook likely serves as a tool for executing various tasks related to checking, fetching, and searching within the project's architecture.</td>
					</tr>
					<tr>
						<td><b><a href='/apps/notebooks/google.ipynb'>google.ipynb</a></b></td>
						<td>- Generates search results based on user queries using the Google Custom Search API<br>- Additionally, defines and retrieves task types for the project.</td>
					</tr>
					</table>
				</blockquote>
			</details>
		</blockquote>
	</details>
</details>

---
## 🚀 Getting Started

### ☑️ Prerequisites

Before getting started with , ensure your runtime environment meets the following requirements:

- **Programming Language:** Python
- **Package Manager:** Pip, Poetry
- **Container Runtime:** Docker


### ⚙️ Installation

Install  using one of the following methods:

**Build from source:**

1. Clone the  repository:
```sh
❯ git clone ../
```

2. Navigate to the project directory:
```sh
❯ cd 
```

3. Install the project dependencies:


**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pip install -r requirements.txt, apps/agent/requirements.txt
```


**Using `poetry`** &nbsp; [<img align="center" src="https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json" />](https://python-poetry.org/)

```sh
❯ poetry install
```


**Using `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker build -t / .
```




### 🤖 Usage
Run  using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ python {entrypoint}
```


**Using `poetry`** &nbsp; [<img align="center" src="https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json" />](https://python-poetry.org/)

```sh
❯ poetry run python {entrypoint}
```


**Using `docker`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Docker-2CA5E0.svg?style={badge_style}&logo=docker&logoColor=white" />](https://www.docker.com/)

```sh
❯ docker run -it {image_name}
```


### 🧪 Testing
Run the test suite using the following command:
**Using `pip`** &nbsp; [<img align="center" src="https://img.shields.io/badge/Pip-3776AB.svg?style={badge_style}&logo=pypi&logoColor=white" />](https://pypi.org/project/pip/)

```sh
❯ pytest
```


**Using `poetry`** &nbsp; [<img align="center" src="https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json" />](https://python-poetry.org/)

```sh
❯ poetry run pytest
```


---
## 📌 Project Roadmap

- [X] **`Task 1`**: <strike>Implement feature one.</strike>
- [ ] **`Task 2`**: Implement feature two.
- [ ] **`Task 3`**: Implement feature three.

---

## 🔰 Contributing

- **💬 [Join the Discussions](https://LOCAL///discussions)**: Share your insights, provide feedback, or ask questions.
- **🐛 [Report Issues](https://LOCAL///issues)**: Submit bugs found or log feature requests for the `` project.
- **💡 [Submit Pull Requests](https://LOCAL///blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your LOCAL account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone .
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to LOCAL**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://LOCAL{///}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=/">
   </a>
</p>
</details>

---

## 🎗 License

This project is protected under the [SELECT-A-LICENSE](https://choosealicense.com/licenses) License. For more details, refer to the [LICENSE](https://choosealicense.com/licenses/) file.

---

## 🙌 Acknowledgments

- List any resources, contributors, inspiration, etc. here.

---
