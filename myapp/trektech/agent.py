import logging
import time
# for Palm
from langchain.llms import GooglePalm
# for OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain
from .templates import (
    ValidationTemplate,
    ItineraryTemplate,
    MappingTemplate,
)

logging.basicConfig(level=logging.INFO)

# Disabling the logger for now 
logger = logging.getLogger('my-logger')
logger.propagate = False

class Agent(object):
    def __init__(
        self,
        open_ai_api_key,
        model="gpt-3.5-turbo",
        temperature=0,
        debug=False,
    ):
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        self._openai_key = open_ai_api_key

        self.chat_model = ChatOpenAI(model=model, temperature=temperature, openai_api_key=self._openai_key)
        self.validation_prompt = ValidationTemplate()
        self.validation_chain = self._set_up_validation_chain(debug)

        self.itinerary_prompt = ItineraryTemplate()
        self.mapping_prompt = MappingTemplate()
        self.agent_chain = self._set_up_agent_chain(debug)


    def _set_up_validation_chain(self, debug=False):
    
        # make validation agent chain
        validation_agent = LLMChain(
            llm=self.chat_model,
            prompt=self.validation_prompt.chat_prompt,
            output_parser=self.validation_prompt.parser,
            output_key="validation_output",
            verbose=debug,
        )
        
        # add to sequential chain 
        overall_chain = SequentialChain(
            chains=[validation_agent], 
            input_variables=["query", "format_instructions"],
            output_variables=["validation_output"],
            verbose=debug,
        )

        return overall_chain

    def validate_travel(self, query):
        self.logger.info("Validating query")
        t1 = time.time()
        self.logger.info(
            "Calling validation (model is {}) on user input".format(
                self.chat_model.model_name
            )
        )
        validation_result = self.validation_chain(
            {
                "query": query,
                "format_instructions": self.validation_prompt.parser.get_format_instructions(),
            }
        )

        validation_test = validation_result["validation_output"].dict()
        t2 = time.time()
        self.logger.info("Time to validate request: {}".format(round(t2 - t1, 2)))

        return validation_test

    def _set_up_agent_chain(self, debug=False):
        
        # set up LLMChain to get the itinerary as a string
        travel_agent = LLMChain(
                llm=self.chat_model,
                prompt=self.itinerary_prompt.chat_prompt,
                verbose=debug,
                output_key="agent_suggestion",
            )
        
        # set up LLMChain to extract the waypoints as a JSON object
        parser = LLMChain(
                llm=self.chat_model,
                prompt=self.mapping_prompt.chat_prompt,
                output_parser=self.mapping_prompt.parser,
                verbose=debug,
                output_key="mapping_list",
            )
        
        # overall chain allows us to call the travel_agent and parser in
        # sequence, with labelled outputs.
        overall_chain = SequentialChain(
                chains=[travel_agent, parser],
                input_variables=["query", "format_instructions"],
                output_variables=["agent_suggestion", "mapping_list"],
                verbose=debug,
            )

        return overall_chain
    def suggest_travel(self, query):
        mapping_prompt = MappingTemplate()

        agent_result = self.agent_chain(
                        {
                            "query": query,
                            "format_instructions": mapping_prompt.parser.get_format_instructions(),
                        }
                    )

        trip_suggestion = agent_result["agent_suggestion"]
        waypoints_dict = agent_result["mapping_list"].dict() 

        return trip_suggestion, waypoints_dict, agent_result          

# FINAL FUNCTIONS TO USE BELOW


def validate(open_ai_api_key,query):
    """
    This function takes a query and returns a json object describing whether a query is valid. 

    EXAMPLE:
    query:
        I want to do a 5 day roadtrip from Cape Town to Pretoria in South Africa.
    result:
        {'plan_is_valid': 'yes', 'updated request': 'none'}

    query:
        I want to walk from Cape Town to Pretoria in South Africa.
    result:
        {'plan_is_valid': 'no','updated_request': 'Walking from Cape Town to Pretoria in South Africa is not a reasonable request...'}
    """
    travel_agent = Agent(open_ai_api_key,debug=False)
    return travel_agent.validate_travel(query)

def suggest(openai_api_key, query):
    travel_agent = Agent(
        open_ai_api_key=openai_api_key,
    )

    itinerary, list_of_places, validation = travel_agent.suggest_travel(query)

    return itinerary, list_of_places, validation