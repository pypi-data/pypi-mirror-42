#ifndef OCCA_CORE_KERNEL_HEADER
#define OCCA_CORE_KERNEL_HEADER

#include <iostream>
#include <stdint.h>
#include <vector>

#include <occa/defines.hpp>
#include <occa/core/kernelArg.hpp>
#include <occa/lang/kernelMetadata.hpp>
#include <occa/tools/gc.hpp>
#include <occa/tools/properties.hpp>
#include <occa/types.hpp>

namespace occa {
  class modeKernel_t; class kernel;
  class modeMemory_t; class memory;
  class modeDevice_t; class device;
  class kernelBuilder;

  namespace lang {
    class parser_t;
  }

  typedef std::map<hash_t, kernel>            hashedKernelMap;
  typedef hashedKernelMap::iterator           hashedKernelMapIterator;
  typedef hashedKernelMap::const_iterator     cHashedKernelMapIterator;

  typedef std::vector<kernelBuilder>          kernelBuilderVector;
  typedef kernelBuilderVector::iterator       kernelBuilderVectorIterator;
  typedef kernelBuilderVector::const_iterator cKernelBuilderVectorIterator;


  //---[ modeKernel_t ]---------------------
  class modeKernel_t : public gc::ringEntry_t {
  public:
    occa::modeDevice_t *modeDevice;

    std::string name;
    std::string sourceFilename, binaryFilename;
    occa::properties properties;

    gc::ring_t<kernel> kernelRing;

    dim outerDims, innerDims;

    std::vector<kernelArgData> arguments;
    lang::kernelMetadata metadata;

    modeKernel_t(modeDevice_t *modeDevice_,
                 const std::string &name_,
                 const std::string &sourceFilename_,
                 const occa::properties &properties_);

    void dontUseRefs();
    void addKernelRef(kernel *ker);
    void removeKernelRef(kernel *ker);
    bool needsFree() const;

    void assertArgumentLimit() const;
    void assertArgInDevice(const kernelArgData &arg) const;

    void setArguments(kernelArg *args,
                      const int count);
    void pushArgument(const kernelArg &arg);

    void setMetadata(lang::parser_t &parser);

    void setupRun();

    //---[ Virtual Methods ]------------
    virtual ~modeKernel_t() = 0;

    virtual int maxDims() const = 0;
    virtual dim maxOuterDims() const = 0;
    virtual dim maxInnerDims() const = 0;

    virtual void run() const = 0;
    //==================================
  };
  //====================================

  //---[ kernel ]-----------------------
  class kernel : public gc::ringEntry_t {
    friend class occa::modeKernel_t;
    friend class occa::device;

  private:
    modeKernel_t *modeKernel;

  public:
    kernel();
    kernel(modeKernel_t *modeKernel_);

    kernel(const kernel &k);
    kernel& operator = (const kernel &k);
    kernel& operator = (modeKernel_t *modeKernel_);
    ~kernel();

  private:
    void assertInitialized() const;
    void setModeKernel(modeKernel_t *modeKernel_);
    void removeKernelRef();

  public:
    void dontUseRefs();

    bool isInitialized();

    const std::string& mode() const;
    const occa::properties& properties() const;

    modeKernel_t* getModeKernel() const;

    occa::device getDevice();

    bool operator == (const occa::kernel &other) const;
    bool operator != (const occa::kernel &other) const;

    const std::string& name();
    const std::string& sourceFilename();
    const std::string& binaryFilename();

    int maxDims();
    dim maxOuterDims();
    dim maxInnerDims();

    void setRunDims(dim outerDims, dim innerDims);

    void pushArg(const kernelArg &arg);
    void clearArgs();

    void run() const;

#include "kernelOperators.hpp"

    void free();
  };
  //====================================

  //---[ kernelBuilder ]----------------
  class kernelBuilder {
  protected:
    std::string source_;
    std::string function_;
    occa::properties props_;

    hashedKernelMap kernelMap;

    bool buildingFromFile;

  public:
    kernelBuilder();

    kernelBuilder(const kernelBuilder &k);
    kernelBuilder& operator = (const kernelBuilder &k);

    static kernelBuilder fromFile(const std::string &filename,
                                  const std::string &function,
                                  const occa::properties &props = occa::properties());

    static kernelBuilder fromString(const std::string &content,
                                    const std::string &function,
                                    const occa::properties &props = occa::properties());

    bool isInitialized();

    occa::kernel build(occa::device device);

    occa::kernel build(occa::device device,
                       const occa::properties &props);

    occa::kernel build(occa::device device,
                       const hash_t &hash);

    occa::kernel build(occa::device device,
                       const hash_t &hash,
                       const occa::properties &props);

    occa::kernel operator [] (occa::device device);

    void free();
  };
  //====================================


  //---[ Kernel Properties ]------------
  hash_t kernelHeaderHash(const occa::properties &props);

  std::string assembleKernelHeader(const occa::properties &props);
  //====================================
}

#endif
