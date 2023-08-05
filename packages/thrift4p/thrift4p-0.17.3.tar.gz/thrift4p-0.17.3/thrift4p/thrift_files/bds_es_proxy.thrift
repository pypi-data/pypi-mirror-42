namespace java com.didachuxing.bigdata.es.proxy.service

service ESProxyService {

    list<string> getIndexList()
    list<string> getMappingList()
    string getMappingInfoByIndexName(1:string indexNmae)
    string putIndex(1:string indexInfo)
    string putMappingToIndex(1:string mappingInfo)
    string deleteIndex(1:string indexNmae)
    string deleteMapping(1:string mappingName)
    string insertInfo(1:string dataInfo)
    list<string> selectInfo(1:string quaryInfo)
    list<string> selectInfoWithTime(1:string index, 2:string parameter, 3:string startTime, 4:string endTime)

}
