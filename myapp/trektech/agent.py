import logging
import time
# for Palm
from langchain.llms import GooglePalm
# for OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain, SequentialChain
from myapp.trektech.templates import (
    ValidationTemplate,
    ItineraryTemplate,
    ItineraryTemplate_v2,
    MappingTemplate,
    UpdateTemplate
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
        self.itinerary_prompt_v2 = ItineraryTemplate_v2()
        self.mapping_prompt = MappingTemplate()
        self.update_prompt = UpdateTemplate()

        self.agent_chain = self._set_up_agent_chain(debug)
        self.agent_chain2 = self._set_up_agent_chain2(debug)
        self.agent_chain3 = self._set_up_agent_chain3(debug)


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
        self.logger.info("Validating query...")
        t1 = time.time()

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
    
    def _set_up_agent_chain2(self, debug=False):

        # set up LLMChain to get the itinerary as a string
        travel_agent = LLMChain(
                llm=self.chat_model,
                prompt=self.itinerary_prompt_v2.chat_prompt,
                verbose=debug,
                output_key="agent_suggestion",
            )
        
        # overall chain allows us to call the travel_agent and parser in
        # sequence, with labelled outputs.
        overall_chain = SequentialChain(
                chains=[travel_agent],
                input_variables=["query"],
                output_variables=["agent_suggestion"],
                verbose=debug,
            )

        return overall_chain
    
    def _set_up_agent_chain3(self, debug=False):
    
        # set up LLMChain to get the itinerary as a string
        travel_agent = LLMChain(
                llm=self.chat_model,
                prompt=self.update_prompt.chat_prompt,
                verbose=debug,
                output_key="agent_suggestion",
            )
        
        # overall chain allows us to call the travel_agent and parser in
        # sequence, with labelled outputs.
        overall_chain = SequentialChain(
                chains=[travel_agent],
                input_variables=["itinerary", "update_query"],
                output_variables=["agent_suggestion"],
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
    
    def suggest_itinerary(self, query):

        self.logger.info("Suggesting information...")
        t1 = time.time()

        agent_result = self.agent_chain2(
                        {
                            "query": query,
                        }
                    )

        trip_suggestion = agent_result["agent_suggestion"]

        t2 = time.time()
        self.logger.info("Time to suggest travel plan: {}".format(round(t2 - t1, 2)))

        return trip_suggestion    
    
    def update_itinerary(self, itinerary, update_query):
    
        self.logger.info("Updating information...")
        t1 = time.time()

        agent_result = self.agent_chain3(
                        {
                            "itinerary": itinerary,
                            "update_query": update_query
                        }
                    )

        updated_suggestion = agent_result["agent_suggestion"]

        t2 = time.time()
        self.logger.info("Time to update travel plan: {}".format(round(t2 - t1, 2)))

        return updated_suggestion  