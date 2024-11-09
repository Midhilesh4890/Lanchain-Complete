import logging
from langchain_community.document_loaders import WikipediaLoader, ArxivLoader, WebBaseLoader, TextLoader, PyPDFLoader
import bs4

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class DocumentLoader:
    def __init__(self, loader_type, source, **kwargs):
        self.loader_type = loader_type
        self.source = source
        self.kwargs = kwargs
        self.loader = self._initialize_loader()

    def _initialize_loader(self):
        try:
            if self.loader_type == 'text':
                return TextLoader(self.source)
            elif self.loader_type == 'pdf':
                return PyPDFLoader(self.source)
            elif self.loader_type == 'web':
                return WebBaseLoader(web_paths=(self.source,), **self.kwargs)
            elif self.loader_type == 'arxiv':
                return ArxivLoader(query=self.source, **self.kwargs)
            elif self.loader_type == 'wikipedia':
                return WikipediaLoader(query=self.source, **self.kwargs)
            else:
                logger.error(f"Invalid loader type: {self.loader_type}")
                raise ValueError(f"Invalid loader type: {self.loader_type}")
        except Exception as e:
            logger.error(f"Error initializing loader: {e}")
            raise

    def load_documents(self):
        try:
            documents = self.loader.load()
            logger.info(
                f"Loaded {len(documents)} documents using {self.loader_type} loader.")
            return documents
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            raise


def load_local_text(file_path):
    text_loader = DocumentLoader(loader_type='text', source=file_path)
    return text_loader.load_documents()


def load_pdf(file_path):
    pdf_loader = DocumentLoader(loader_type='pdf', source=file_path)
    return pdf_loader.load_documents()


def load_web_content(url, parse_classes):
    web_loader = DocumentLoader(
        loader_type='web',
        source=url,
        bs_kwargs=dict(parse_only=bs4.SoupStrainer(class_=parse_classes))
    )
    return web_loader.load_documents()


def load_arxiv(query, max_docs):
    arxiv_loader = DocumentLoader(
        loader_type='arxiv', source=query, load_max_docs=max_docs)
    return arxiv_loader.load_documents()


def load_wikipedia(query, max_docs):
    wiki_loader = DocumentLoader(
        loader_type='wikipedia', source=query, load_max_docs=max_docs)
    return wiki_loader.load_documents()


if __name__ == "__main__":
    # Load text file
    text_documents = load_local_text("speech.txt")

    # Load PDF file
    pdf_documents = load_pdf("attention.pdf")

    # Load web content
    web_documents = load_web_content(
        url="https://lilianweng.github.io/posts/2023-06-23-agent/",
        parse_classes=["post-title", "post-content", "post-header"]
    )

    # Load Arxiv documents
    arxiv_docs = load_arxiv(query="1706.03762", max_docs=2)
    logger.info(f"Arxiv documents loaded: {len(arxiv_docs)}")

    # Load Wikipedia documents
    wiki_docs = load_wikipedia(query="Generative AI", max_docs=2)
    logger.info(f"Wikipedia documents loaded: {len(wiki_docs)}")
